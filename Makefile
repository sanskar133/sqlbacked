DOCKER_HUB_BACKEND_USER = aideticankur
DOCKER_HUB_FRONTEND_USER = naveenkalburgisaidtic
REPO_BACKEND = prequel-ai
REPO_FRONTEND = prequel-ai-fe
BACKEND_PATH = chat_backend
FRONTEND_PATH = fabric_analytics_frontend
BACKEND_DOCKERFILE = $(BACKEND_PATH)/Dockerfile
FRONTEND_DOCKERFILE = $(FRONTEND_PATH)/Dockerfile


check-tag:
	@if [ -z "$(TAG)" ]; then \
		echo "Error: TAG variable is not set"; \
		exit 1; \
	fi

compile:
	@cd chat_backend && chmod +x compile.sh && ./compile.sh

build-image: check-tag compile
	@docker build -f $(BACKEND_DOCKERFILE) -t $(DOCKER_HUB_BACKEND_USER)/$(REPO_BACKEND):$(TAG) $(BACKEND_PATH)
	@docker build -f $(FRONTEND_DOCKERFILE) -t $(DOCKER_HUB_FRONTEND_USER)/$(REPO_FRONTEND):$(TAG) $(FRONTEND_PATH)

run: 
	@echo "Running all Images"
	@TAG=$(TAG) \
	DOCKER_HUB_BACKEND_USER=$(DOCKER_HUB_BACKEND_USER) \
	REPO_BACKEND=$(REPO_BACKEND) \
	DOCKER_HUB_FRONTEND_USER=$(DOCKER_HUB_FRONTEND_USER) \
	REPO_FRONTEND=$(REPO_FRONTEND) \
	docker compose -f docker-compose.prod.yml up -d

push-image: check-tag 
	@echo "Pushing Backend Image"
	@docker login -u $(DOCKER_HUB_BACKEND_USER) -p $(TOKEN_BE)
	@docker push $(DOCKER_HUB_BACKEND_USER)/$(REPO_BACKEND):$(TAG)
	@docker logout

	@echo "Pushing Frontend Image"
	@docker login -u $(DOCKER_HUB_FRONTEND_USER) -p $(TOKEN_FE)
	@docker push $(DOCKER_HUB_FRONTEND_USER)/$(REPO_FRONTEND):$(TAG)
	@docker logout

pull-run: check-tag
	@echo "Pulling Backend Image"
	@docker login -u $(DOCKER_HUB_BACKEND_USER) -p $(TOKEN_BE)
	@docker pull $(DOCKER_HUB_BACKEND_USER)/$(REPO_BACKEND):$(TAG)
	@docker logout

	@echo "Pulling Frontend Image"
	@docker login -u $(DOCKER_HUB_FRONTEND_USER) -p $(TOKEN_FE)
	@docker pull $(DOCKER_HUB_FRONTEND_USER)/$(REPO_FRONTEND):$(TAG)
	@docker logout

	@$(MAKE) --no-print-directory run TAG=$(TAG)