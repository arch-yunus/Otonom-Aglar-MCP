.PHONY: help install test docker-up docker-down clean run-client

help: ## Mevcut Makefile komutlarını listeler
	@echo "Mevcut Komutlar:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Bağımlılıkları yerel ortama yükler
	pip install -r requirements.txt

test: ## Otomatik PyTest senaryolarını çalıştırır
	pytest tests/ -v

docker-up: ## Tüm ajan sunucularını arka planda Docker ile ayağa kaldırır
	docker compose up -d

docker-down: ## Ayağa kalkan Docker ajanlarını durdurur
	docker compose down

run-client: ## Modül 5'teki örnek MCP İstemcisini (Host) test amacıyla çalıştırır
	python src/05_mcp_client_example/simple_agent.py

clean: ## Logları, önbellek (cache) ve gereksiz dosyaları temizler
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -f agent_memory.json
