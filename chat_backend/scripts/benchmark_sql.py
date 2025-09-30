import os
import re

import pandas as pd
from joblib import Parallel, delayed
from pandas.testing import assert_frame_equal, assert_series_equal

#############################################################
# setup done
#############################################################


#################################
# COMPARE funcs
#################################
def normalize_table(
    df: pd.DataFrame, query_category: str, question: str, sql: str = None
) -> pd.DataFrame:
    """
    Normalizes a dataframe by:
    1. removing all duplicate rows
    2. sorting columns in alphabetical order
    3. sorting rows using values from first column to last (if query_category is not 'order_by' and question does not ask for ordering)
    4. resetting index
    """
    # remove duplicate rows, if any
    df = df.drop_duplicates()

    # sort columns in alphabetical order of column names
    sorted_df = df.reindex(sorted(df.columns), axis=1)

    # check if query_category is 'order_by' and if question asks for ordering
    has_order_by = False
    pattern = re.compile(r"\b(order|sort|arrange)\b", re.IGNORECASE)
    in_question = re.search(pattern, question.lower())  # true if contains
    if query_category == "order_by" or in_question:
        has_order_by = True

        if sql:
            # determine which columns are in the ORDER BY clause of the sql generated, using regex
            pattern = re.compile(r"ORDER BY[\s\S]*", re.IGNORECASE)
            order_by_clause = re.search(pattern, sql)
            if order_by_clause:
                order_by_clause = order_by_clause.group(0)
                # get all columns in the ORDER BY clause, by looking at the text between ORDER BY and the next semicolon, comma, or parantheses
                pattern = re.compile(r"(?<=ORDER BY)(.*?)(?=;|,|\)|$)", re.IGNORECASE)
                order_by_columns = re.findall(pattern, order_by_clause)
                order_by_columns = (
                    order_by_columns[0].split() if order_by_columns else []
                )
                order_by_columns = [
                    col.strip().rsplit(".", 1)[-1] for col in order_by_columns
                ]

                ascending = False
                # if there is a DESC or ASC in the ORDER BY clause, set the ascending to that
                if "DESC" in [i.upper() for i in order_by_columns]:
                    ascending = False
                elif "ASC" in [i.upper() for i in order_by_columns]:
                    ascending = True

                # remove whitespace, commas, and parantheses
                order_by_columns = [col.strip() for col in order_by_columns]
                order_by_columns = [
                    col.replace(",", "").replace("(", "") for col in order_by_columns
                ]
                order_by_columns = [
                    i
                    for i in order_by_columns
                    if i.lower()
                    not in ["desc", "asc", "nulls", "last", "first", "limit"]
                ]

                # get all columns in sorted_df that are not in order_by_columns
                other_columns = [
                    i for i in sorted_df.columns.tolist() if i not in order_by_columns
                ]

                # only choose order_by_columns that are in sorted_df
                order_by_columns = [
                    i for i in order_by_columns if i in sorted_df.columns.tolist()
                ]
                sorted_df = sorted_df.sort_values(
                    by=order_by_columns + other_columns, ascending=ascending
                )

    if not has_order_by:
        # sort rows using values from first column to last
        sorted_df = sorted_df.sort_values(by=list(sorted_df.columns))

    # reset index
    sorted_df = sorted_df.reset_index(drop=True)
    return sorted_df


def compare_df(
    df_gold: pd.DataFrame,
    df_gen: pd.DataFrame,
    query_category: str,
    question: str,
    query_gold: str = None,
    query_gen: str = None,
) -> bool:
    """
    Compares two dataframes and returns True if they are the same, else False.
    query_gold and query_gen are the original queries that generated the respective dataframes.
    """
    # stop early if shapes do not match
    if df_gold.shape != df_gen.shape:
        return False

    # drop duplicates to ensure equivalence
    is_equal = df_gold.values == df_gen.values
    try:
        if is_equal.all():
            return True
    except:
        if is_equal:
            return True

    df_gold = normalize_table(df_gold, query_category, question, query_gold)
    df_gen = normalize_table(df_gen, query_category, question, query_gen)

    # perform same checks again for normalized tables
    if df_gold.shape != df_gen.shape:
        return False

    is_equal = df_gold.values == df_gen.values
    try:
        return is_equal.all()
    except:
        return is_equal


def subset_df(
    df_sub: pd.DataFrame,
    df_super: pd.DataFrame,
    query_category: str,
    question: str,
    query_super: str = None,
    query_sub: str = None,
    verbose: bool = False,
) -> bool:
    """
    Checks if df_sub is a subset of df_super.
    """
    if df_sub.empty:
        return False  # handle cases for empty dataframes

    # make a copy of df_super so we don't modify the original while keeping track of matches
    df_super_temp = df_super.copy(deep=True)
    matched_columns = []
    for col_sub_name in df_sub.columns:
        col_match = False
        for col_super_name in df_super_temp.columns:
            col_sub = df_sub[col_sub_name].sort_values().reset_index(drop=True)
            col_super = (
                df_super_temp[col_super_name].sort_values().reset_index(drop=True)
            )

            try:
                assert_series_equal(
                    col_sub, col_super, check_dtype=False, check_names=False
                )
                col_match = True
                matched_columns.append(col_super_name)
                # remove col_super_name to prevent us from matching it again
                df_super_temp = df_super_temp.drop(columns=[col_super_name])
                break
            except AssertionError:
                continue
            except Exception as e:
                print(e)
                continue

        if not col_match:
            if verbose:
                print(f"no match for {col_sub_name}")
            return False

    df_sub_normalized = normalize_table(df_sub, query_category, question, query_sub)

    # get matched columns from df_super, and rename them with columns from df_sub, then normalize
    df_super_matched = df_super[matched_columns].rename(
        columns=dict(zip(matched_columns, df_sub.columns))
    )
    df_super_matched = normalize_table(
        df_super_matched, query_category, question, query_super
    )

    try:
        assert_frame_equal(df_sub_normalized, df_super_matched, check_dtype=False)
        return True
    except AssertionError:
        return False


# function from sql-eval repo
def compare_query_results(
    query_gold: str,
    query_gen: str,
    results_gold: pd.DataFrame,
    results_gen: pd.DataFrame,
    question: str,
    query_category: str,
    table_metadata_string: str = "",
    timeout: float = 10.0,
    decimal_points: int = None,
) -> "tuple[bool, bool]":
    """
    Compares the results of two queries and returns a tuple of booleans, where the first element is
    whether the queries produce exactly the same result, and the second element is whether the
    result of the gold query is a subset of the result of the generated query (still correct).
    We bubble up exceptions (mostly from query_postgres_db) to be handled in the runner.
    """
    # TODO currently no gold queries are there, can introduce gold queries
    # queries_gold = get_all_minimal_queries(query_gold)
    queries_gold = [query_gold]

    correct = False
    for q in queries_gold:
        # TODO: get results of each minimal query from gold query

        if compare_df(
            results_gold, results_gen, query_category, question, query_gold, query_gen
        ):
            return (True, True)
        elif subset_df(results_gold, results_gen, query_category, question):
            correct = True
    return (False, correct)


############################################################


def run_chat_flow_for_given_question(question: str):
    user_id = "prequel_ai_4521"
    from chat_manager.v5 import ChatManagerV5 as ChatManager
    from databases import utils as database_connection_management_utils
    from interface import WebsocketRequest
    from settings import env

    connection_metadata = env.CONNECTION_META_DATA[user_id]
    connection_type = "STANDARD"
    database_object = database_connection_management_utils.get_database_object(
        connection_metadata["database_type"],
        connection_metadata["database_meta_data"],
        connection_type=connection_type,
    )
    request_obj = WebsocketRequest(
        chat_session_id="sessionid",
        user_id=user_id,
        message=question,
        history=[],
    )
    chat_manager = ChatManager(database_object, request_obj, "socket-id", True)

    query_output, step_data = chat_manager.run(request_obj, "temp-id")

    results_gen = query_output[0].get("data")
    return results_gen, step_data


def run_gold_query(query_gold: str):
    user_id = "prequel_ai_4521"
    from chat_manager.v5 import ChatManagerV5 as ChatManager
    from databases import utils as database_connection_management_utils
    from interface import WebsocketRequest
    from settings import env

    connection_metadata = env.CONNECTION_META_DATA[user_id]
    connection_type = "STANDARD"

    database_object = database_connection_management_utils.get_database_object(
        connection_metadata["database_type"],
        connection_metadata["database_meta_data"],
        connection_type=connection_type,
    )
    request_obj = WebsocketRequest(
        chat_session_id="sessionid",
        user_id=user_id,
        message="dummy question",
        history=[],
    )

    chat_manager = ChatManager(database_object, request_obj, "socket-id", True)
    (
        query_output_gold,
        execute_sql_query_step_data,
    ) = chat_manager.execute_sql_query_object.run(
        "temp_query_id",
        updated_queries=[
            {
                "query_validation_remark": ["temp_value"],
                "query_after_regex_match": query_gold,
            }
        ],
        benchmark=True,
    )
    return query_output_gold.get("data")[0].get("data")


def process_benchmark_row(row, trials=1):
    question = row[1]["question"]
    question_category = row[1]["question_category"]

    results_gen_trials = []
    query_gen_trials = []

    for trial in range(trials):
        try:
            results_gen, step_data = run_chat_flow_for_given_question(question=question)
            results_gen = pd.DataFrame(results_gen)
            try:
                query_gen = (
                    step_data[-2]
                    .data.get("validated_queries")[0]
                    .get("query_after_regex_match")
                )
            except Exception as e:
                query_gen = "Not Generated!"
        except Exception as e:
            results_gen = pd.DataFrame([{"dummy": "dummy"}])
            query_gen = ""
            print(f"Error: {e}. Gen Failed for query: {question}")
        results_gen_trials.append(results_gen)
        query_gen_trials.append(query_gen)

    query_gold = row[1]["query"]

    try:
        results_gold = run_gold_query(query_gold)
        results_gold = pd.DataFrame(results_gold)
    except Exception as e:
        results_gold = pd.DataFrame([{"dummyG": "dummyG"}])
        print(f"Error: {e}. Gold Failed for query: {question}")
    # print(results_gold)

    # print("COMPARISON:")
    exact_match_trials = []
    subset_match_trials = []
    for trial in range(trials):
        exact_match, subset_match = compare_query_results(
            query_gold,
            query_gen_trials[trial],
            results_gold,
            results_gen_trials[trial],
            question,
            question_category,
        )
        exact_match_trials.append(exact_match)
        subset_match_trials.append(subset_match)
    return (
        exact_match_trials,
        subset_match_trials,
        query_gen_trials,
        results_gold,
        results_gen_trials,
    )

    # benchmark_df.loc[row[0], "exact_match"] = exact_match
    # benchmark_df.loc[row[0], "subset_match"] = subset_match
    # print("GEN:")
    # print(query_gen)
    # print(results_gen)

    # print()

    # print("GOLD:")
    # print(query_gold)
    # print(results_gold)

    # break


# read Benchmark dataset
benchmark_df = pd.read_csv(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "benchmark_sql.csv"),
    index_col=0,
)

# benchmark_df["exact_match"] = False
# benchmark_df["subset_match"] = False

trials = 2
results = Parallel(n_jobs=2)(
    delayed(process_benchmark_row)(row, trials) for row in benchmark_df.iterrows()
)

exact_matches, subset_matches, query_gens, results_golds, results_gens = zip(*results)

# benchmark_df["exact_match"] = exact_matches
# benchmark_df["subset_match"] = subset_matches
# benchmark_df["query_gen"] = query_gens
benchmark_df["results_gold"] = results_golds
# benchmark_df["results_gen"] = results_gens

col_name_list = lambda col_name: [f"{col_name}_{trial+1}" for trial in range(trials)]

benchmark_df[col_name_list("exact_match")] = pd.DataFrame(
    exact_matches, index=benchmark_df.index
)
benchmark_df[col_name_list("subset_match")] = pd.DataFrame(
    subset_matches, index=benchmark_df.index
)
benchmark_df[col_name_list("query_gen")] = pd.DataFrame(
    query_gens, index=benchmark_df.index
)
benchmark_df[col_name_list("results_gen")] = pd.DataFrame(
    results_gens, index=benchmark_df.index
)

benchmark_df["subset_trials_sum"] = benchmark_df[col_name_list("subset_match")].sum(
    axis=1
)
benchmark_df["no_trials"] = trials

print(benchmark_df)

benchmark_df.to_csv(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "benchmark_sql_post_run.csv"
    )
)


print("Total Queries:", benchmark_df.shape)
print("Exact Match:\n", benchmark_df["exact_match_1"].value_counts())
print("\nSubset Match:\n", benchmark_df["subset_match_1"].value_counts())
print(
    f"\n\nAccuracy: {benchmark_df['subset_trials_sum'].sum() / benchmark_df['no_trials'].sum() * 100 }"
)
