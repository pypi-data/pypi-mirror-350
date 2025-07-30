"""Constants used throughout the package."""

# API endpoints
DEFAULT_BASE_URL = "http://localhost:11434"
OLLAMA_API_BASE = DEFAULT_BASE_URL
OLLAMA_API_GENERATE = f"{OLLAMA_API_BASE}/api/generate"
OLLAMA_API_CHAT = f"{OLLAMA_API_BASE}/api/chat"
OLLAMA_API_EMBEDDINGS = f"{OLLAMA_API_BASE}/api/embeddings"
OLLAMA_API_PULL = f"{OLLAMA_API_BASE}/api/pull"
OLLAMA_API_PUSH = f"{OLLAMA_API_BASE}/api/push"
OLLAMA_API_LIST = f"{OLLAMA_API_BASE}/api/tags"
OLLAMA_API_SHOW = f"{OLLAMA_API_BASE}/api/show"
OLLAMA_API_DELETE = f"{OLLAMA_API_BASE}/api/delete"
OLLAMA_API_COPY = f"{OLLAMA_API_BASE}/api/copy"

# Model defaults
DEFAULT_MODEL = "llama2"
DEFAULT_NUM_CTX = 4096
DEFAULT_NUM_THREAD = 4
DEFAULT_NUM_GPU = 1
DEFAULT_BATCH_SIZE = 512
DEFAULT_SEED = 42
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.9
DEFAULT_TOP_K = 40
DEFAULT_REPEAT_PENALTY = 1.1
DEFAULT_REPEAT_LAST_N = 64
DEFAULT_STOP = None
DEFAULT_TIMEOUT = 120
DEFAULT_STREAM = True

# Supported file types
SUPPORTED_TEXT_FORMATS = ['.txt', '.md', '.rst', '.py', '.js', '.html', '.css', '.json', '.xml', '.yaml', '.yml']
SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
SUPPORTED_DOCUMENT_FORMATS = ['.pdf', '.doc', '.docx', '.odt', '.rtf']
SUPPORTED_SPREADSHEET_FORMATS = ['.csv', '.xls', '.xlsx', '.ods']
SUPPORTED_PRESENTATION_FORMATS = ['.ppt', '.pptx', '.odp']
SUPPORTED_ARCHIVE_FORMATS = ['.zip', '.tar', '.gz', '.rar', '.7z']
SUPPORTED_CODE_FORMATS = [
    '.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.go', '.rb', '.php', '.swift', '.kt', '.rs', '.scala', '.pl', '.sh', '.bat', '.ps1', '.lua', '.r', '.m', '.jl', '.dart', '.sql', '.html', '.css', '.json', '.xml', '.yaml', '.yml'
]
SUPPORTED_BINARY_FORMATS = ["bin", "dat", "model", "weights"]

# Supported models
SUPPORTED_MODELS = [
    "llama2",
    "mistral",
    "gpt-3.5-turbo",
    "gpt-4",
    "vicuna",
    "falcon",
    "bloom",
    "dolly",
    "openllama",
    "phi",
    "mixtral",
]

# Supported roles
SUPPORTED_ROLES = ["system", "user", "assistant"]

# Logging
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_LOG_FILE = "evolvishub_ollama_adapter.log"
DEFAULT_LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
DEFAULT_LOG_BACKUP_COUNT = 5

# Database
DEFAULT_DB_HOST = "localhost"
DEFAULT_DB_PORT = 27017
DEFAULT_DB_NAME = "evolvishub_ollama_adapter"
DEFAULT_DB_USER = None
DEFAULT_DB_PASSWORD = None
DEFAULT_DB_URI = None

# Cache
DEFAULT_CACHE_TTL = 3600
DEFAULT_CACHE_MAX_SIZE = 1000
DEFAULT_CACHE_DIR = ".cache"

# Timeouts
DEFAULT_CONNECT_TIMEOUT = 10
DEFAULT_READ_TIMEOUT = 30
DEFAULT_WRITE_TIMEOUT = 30

# Retry
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 1
DEFAULT_RETRY_BACKOFF = 2

# Validation
MAX_CHUNK_SIZE = 8192
MAX_OVERLAP = 1024
MAX_BATCH_SIZE = 1024
MAX_TIMEOUT = 300
MAX_RETRIES = 10

# New constants
DEFAULT_TEXT_CHUNK_SIZE = 1024
DEFAULT_MAX_TOKENS = 2048
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB in bytes
MAX_TEXT_LENGTH = 1000000  # Maximum length of text input
DEFAULT_TEXT_CHUNK_OVERLAP = 100
DEFAULT_IMAGE_MAX_SIZE = 10 * 1024 * 1024  # 10MB in bytes
DEFAULT_IMAGE_QUALITY = 95

# Supported options
SUPPORTED_OPTIONS = [
    "temperature",
    "top_p",
    "top_k",
    "repeat_penalty",
    "max_tokens",
    "num_ctx",
    "num_thread",
    "num_gpu",
    "batch_size",
    "seed",
    "timeout",
    "stream"
] 