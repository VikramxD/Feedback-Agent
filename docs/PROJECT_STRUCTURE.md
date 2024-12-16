# ML Model Serving Infrastructure

## Overview
This codebase focuses on ML model serving in production, specifically handling voice processing, emotion analysis, and text processing pipelines.

```
ml-serving/
├── src/                    # Source code
│   ├── models/            # ML model definitions and inference
│   │   ├── voice/        # Voice processing models
│   │   ├── emotion/      # Emotion analysis models
│   │   └── text/         # Text processing models
│   ├── pipeline/          # Processing pipeline
│   │   ├── processor/    # Message processing
│   │   └── queue/        # Queue management
│   └── utils/             # Shared utilities
├── config/                # Configuration files
│   ├── model_config/     # Model configurations
│   └── pipeline_config/  # Pipeline settings
├── scripts/              # Processing scripts
│   ├── voice2text/      # Voice to text conversion
│   └── preprocessing/    # Data preprocessing
└── tests/                # Test suites

## Directory Details

### src/models/
- Model inference code
- Model versioning
- Model loading and serving

### src/pipeline/
- Message queue consumer
- Processing pipeline
- Error handling
- Logging and monitoring

### scripts/
- Voice processing scripts
- Data preprocessing utilities
- Model serving scripts

### config/
- Model configurations
- Processing pipeline settings
- Environment configurations

### tests/
- Unit tests for models
- Integration tests for pipeline
- Performance tests
