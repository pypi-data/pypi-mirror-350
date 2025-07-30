"""
Example services demonstrating different registration patterns.
"""

from fastapi import APIRouter, HTTPException

from consul_registration import register_indexer, register_service, register_worker


# Example 1: Worker Service with router class
@register_worker("pdf-processor")
class PDFProcessorService:
    """Example worker service that processes PDFs."""

    router = APIRouter(prefix="/api/workers/v1")

    def __init__(self):
        self.processing_queue: list[str] = []
        self._setup_routes()

    def _setup_routes(self):
        @self.router.post("/process")
        async def process_pdf(file_path: str):
            """Queue a PDF for processing."""
            self.processing_queue.append(file_path)
            return {"status": "queued", "file": file_path, "position": len(self.processing_queue)}

        @self.router.get("/status")
        async def get_status():
            """Get worker status."""
            return {"status": "active", "queue_size": len(self.processing_queue), "service": "pdf-processor"}


# Example 2: Indexer Service with direct router decoration
search_router = APIRouter(prefix="/api/indexers/v1")


@register_indexer("document-indexer")
class DocumentIndexerService:
    """Example indexer service for document search."""

    router = search_router
    documents: dict[str, dict] = {}

    @staticmethod
    @search_router.post("/index")
    async def index_document(doc_id: str, content: str, metadata: dict = None):
        """Index a document."""
        DocumentIndexerService.documents[doc_id] = {
            "content": content,
            "metadata": metadata or {},
        }
        return {"indexed": True, "doc_id": doc_id}

    @staticmethod
    @search_router.get("/search")
    async def search_documents(query: str):
        """Search indexed documents."""
        results = []
        for doc_id, doc in DocumentIndexerService.documents.items():
            if query.lower() in doc["content"].lower():
                results.append({"doc_id": doc_id, "snippet": doc["content"][:100]})
        return {"query": query, "results": results, "count": len(results)}


# Example 3: General Service with separate router
user_router = APIRouter(prefix="/api/v1")


@register_service("user-service")
class UserService:
    """Example general service for user management."""

    router = user_router
    users: dict[str, dict] = {
        "1": {"id": "1", "name": "Alice", "email": "alice@example.com"},
        "2": {"id": "2", "name": "Bob", "email": "bob@example.com"},
    }

    @staticmethod
    @user_router.get("/users")
    async def list_users():
        """List all users."""
        return {"users": list(UserService.users.values())}

    @staticmethod
    @user_router.get("/users/{user_id}")
    async def get_user(user_id: str):
        """Get a specific user."""
        if user_id not in UserService.users:
            raise HTTPException(status_code=404, detail="User not found")
        return UserService.users[user_id]

    @staticmethod
    @user_router.post("/users")
    async def create_user(name: str, email: str):
        """Create a new user."""
        user_id = str(len(UserService.users) + 1)
        UserService.users[user_id] = {
            "id": user_id,
            "name": name,
            "email": email,
        }
        return UserService.users[user_id]


# Example 4: Service with custom configuration
@register_service(
    name="auth-service",
    base_route="/api/auth/v1",
    health_endpoint="/health",  # Use the shared health endpoint
)
class AuthService:
    """Example authentication service with custom health endpoint."""

    router = APIRouter(prefix="/api/auth/v1")

    @staticmethod
    @router.post("/login")
    async def login(username: str, password: str):
        """Authenticate user."""
        # This is just an example - never check passwords like this in production!
        if username == "admin" and password == "secret":
            return {"token": "fake-jwt-token", "user": username}
        raise HTTPException(status_code=401, detail="Invalid credentials")

    @staticmethod
    @router.get("/health")
    async def health():
        """Custom health endpoint for auth service."""
        return {"status": "healthy", "service": "auth-service"}


# Example 5: Disabled service (won't be registered)
@register_service("disabled-service", base_route="/api/disabled/v1", enabled=False)
class DisabledService:
    """This service won't be registered because enabled=False."""

    router = APIRouter(prefix="/api/disabled/v1")

    @staticmethod
    @router.get("/never-registered")
    async def never_called():
        return {"message": "This endpoint is not registered with Consul"}
