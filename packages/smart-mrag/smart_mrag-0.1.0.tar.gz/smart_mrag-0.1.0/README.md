# Smart MRAG

A powerful AI-powered document analysis system designed specifically for financial professionals. Smart MRAG helps financial analysts quickly extract insights from complex financial documents, research reports, and market data.

## Features

- **Financial Document Analysis**:
  - Extract key financial metrics and ratios from reports
  - Analyze earnings calls transcripts and investor presentations
  - Process complex financial statements and regulatory filings
  - Identify market trends and competitive analysis from research reports

- **Efficient Information Retrieval**:
  - Quickly find relevant sections in lengthy financial documents
  - Compare financial data across multiple reports
  - Extract specific financial metrics and KPIs
  - Analyze historical performance trends

- **Intelligent Financial Querying**:
  - Ask natural language questions about financial data
  - Get detailed analysis of financial statements
  - Compare company performance metrics
  - Analyze market trends and industry benchmarks

- **Multi-Document Analysis**:
  - Compare financial data across multiple companies
  - Analyze industry trends from multiple reports
  - Track changes in financial metrics over time
  - Generate comprehensive market analysis

- **Advanced Financial Insights**:
  - Identify key financial trends and patterns
  - Analyze risk factors and market conditions
  - Extract competitive intelligence
  - Generate investment thesis support

- **Flexible Model Support**: Use any combination of LLM and embedding models
- **Optimized Default Model**: Uses GPT-4o as the default model for optimal performance

## Use Cases for Financial Analysts

### 1. Earnings Analysis
- Quickly analyze earnings reports and transcripts
- Extract key financial metrics and guidance
- Compare actual results with estimates
- Identify important management commentary

### 2. Financial Statement Analysis
- Process and analyze balance sheets, income statements, and cash flow statements
- Calculate and compare financial ratios
- Track changes in key metrics over time
- Identify financial trends and patterns

### 3. Market Research
- Analyze industry reports and market research
- Compare company performance with peers
- Track market trends and competitive dynamics
- Generate investment thesis support

### 4. Regulatory Compliance
- Process and analyze regulatory filings (10-K, 10-Q, etc.)
- Track changes in accounting policies
- Monitor compliance requirements
- Analyze risk factors and disclosures

### 5. Investment Research
- Generate comprehensive company analysis
- Compare investment opportunities
- Track market sentiment and analyst opinions
- Support investment decision-making

## Model Support

### Recommended Model Combinations
1. **OpenAI Models**:
   - **GPT-4o Series** (Default):
     - `gpt-4o`: Optimized for financial document analysis
     - `gpt-4o-mini`: Lightweight version for simpler tasks
     - `gpt-4o-turbo`: Fast and efficient version
   - **GPT-3.5 Series**:
     - `gpt-3.5-turbo`: Standard version, good for general use
     - `gpt-3.5-turbo-16k`: Extended context window (16k tokens)
   - **GPT-4 Series**:
     - `gpt-4`: Standard version, excellent for complex analysis
     - `gpt-4-32k`: Extended context window (32k tokens)
     - `gpt-4-turbo-preview`: Faster and more cost-effective
     - `gpt-4-vision-preview`: Supports image analysis
   - **Embedding Models**:
     - `text-embedding-ada-002`: Standard version, good balance
     - `text-embedding-3-small`: Cost-effective option
     - `text-embedding-3-large`: Highest quality
     - `text-embedding-3-large-256`: Optimized for specific use cases
   - Requires: OpenAI API key

2. **Anthropic Models**:
   - LLM: `claude-3-opus`, `claude-3-sonnet`, `claude-2.1`
   - Embedding: `text-embedding-ada-002`, `text-embedding-3-small`, `text-embedding-3-large`
   - Requires: Anthropic API key + OpenAI API key (for embeddings)

3. **Google Models**:
   - LLM: `gemini-pro`, `gemini-ultra`
   - Embedding: `textembedding-gecko`, `textembedding-gecko-multilingual`
   - Requires: Google API key

### Default Configuration
The system uses GPT-4o as the default model because it:
- Is specifically optimized for financial document analysis
- Provides excellent understanding of financial terminology and concepts
- Offers accurate extraction of financial metrics and data
- Has strong context understanding for complex financial documents
- Is cost-effective for financial analysis tasks

## Installation

```bash
pip install smart-mrag
```

## Usage

### Basic Usage

```python
from smart_mrag import SmartMRAG

# Initialize with default model (GPT-4o)
mrag = SmartMRAG(openai_api_key="your-openai-api-key")

# Load financial documents
mrag.load_document("earnings_report.pdf")
mrag.load_document("annual_report.pdf")

# Ask financial analysis questions
response = mrag.ask("What were the key financial metrics in the earnings report?")
print(response)

# Compare financial data
response = mrag.ask("Compare the revenue growth between the last two quarters")
print(response)
```

### Advanced Financial Analysis

```python
from smart_mrag import SmartMRAG

# Custom configuration for financial analysis
mrag = SmartMRAG(
    # API Keys
    openai_api_key="your-openai-api-key",
    
    # Model Selection
    llm_model="gpt-4o",  # Optimized for financial analysis
    embedding_model="text-embedding-3-large",  # High accuracy for financial data
    
    # Analysis Parameters
    chunk_size=2000,  # Larger chunks for financial context
    chunk_overlap=400,  # More overlap for financial metrics
    similarity_threshold=0.8,  # Higher threshold for financial accuracy
    
    # Advanced Settings
    max_tokens=8000,  # More tokens for detailed analysis
    temperature=0.3,  # Lower temperature for precise financial data
    top_k=5  # More context for financial comparisons
)

# Load multiple financial documents
mrag.load_document("company_10k.pdf")
mrag.load_document("industry_report.pdf")
mrag.load_document("competitor_analysis.pdf")

# Perform complex financial analysis
response = mrag.ask("""
    Analyze the company's financial performance:
    1. Compare revenue growth with industry peers
    2. Identify key risk factors from the 10-K
    3. Extract and analyze key financial ratios
    4. Summarize management's outlook
""")
print(response)
```

## API Key Requirements

The system automatically detects which API keys are required based on your model selection:

1. **OpenAI Models**:
   - Requires: OpenAI API key
   - Example: `gpt-4o` + `text-embedding-3-large`

2. **Anthropic Models**:
   - Requires: Anthropic API key + OpenAI API key
   - Example: `claude-3-opus` + `text-embedding-ada-002`

3. **Google Models**:
   - Requires: Google API key
   - Example: `gemini-pro` + `textembedding-gecko`

4. **Mixed Models**:
   - Requires: All relevant API keys
   - Example: `gpt-4o-turbo` + `textembedding-gecko` (requires both OpenAI and Google API keys)

## Model Selection Guide

### Choosing the Right LLM
- **For Financial Analysis (Recommended)**: `gpt-4o` (optimized for financial documents)
- **For General Analysis**: `gpt-3.5-turbo` (fast, cost-effective)
- **For Complex Analysis**: `gpt-4` or `gpt-4o` (more capable, higher cost)
- **For Large Documents**: `gpt-4-32k` or `gpt-3.5-turbo-16k` (extended context)
- **For Fast Analysis**: `gpt-4o-turbo` or `gpt-4-turbo-preview` (optimized for speed)
- **For Multilingual Analysis**: `gemini-pro` (excellent multilingual support)

### Choosing the Right Embedding Model
- **For General Analysis**: `text-embedding-ada-002` (good balance of performance and cost)
- **For Better Accuracy**: `text-embedding-3-large` (higher quality, higher cost)
- **For Cost Efficiency**: `text-embedding-3-small` (good performance, lower cost)
- **For Specific Analysis**: `text-embedding-3-large-256` (optimized embeddings)
- **For Multilingual Analysis**: `textembedding-gecko-multilingual` (excellent multilingual support)

## Code Robustness and Error Handling

Smart MRAG is built with robust error handling and financial-specific safeguards to ensure reliable analysis:

### 1. Financial Data Validation
- **Data Type Checking**: Validates financial metrics and ratios for correct data types
- **Range Validation**: Ensures financial values are within reasonable ranges
- **Consistency Checks**: Verifies consistency between related financial metrics
- **Format Verification**: Validates financial statement formats and structures

### 2. Document Processing Safeguards
- **PDF Integrity Checks**: Validates PDF structure and content
- **OCR Fallback**: Automatic fallback to OCR for scanned documents
- **Encoding Detection**: Handles various text encodings in financial documents
- **Table Recognition**: Special handling for financial tables and statements

### 3. Error Recovery Mechanisms
- **Graceful Degradation**: Falls back to simpler analysis when complex processing fails
- **Partial Results**: Returns partial analysis when complete analysis isn't possible
- **Retry Logic**: Automatic retries for transient API failures
- **Context Preservation**: Maintains analysis context across retries

### 4. Financial-Specific Error Handling
```python
try:
    # Load and analyze financial document
    mrag.load_document("financial_statement.pdf")
    analysis = mrag.ask("Extract key financial ratios")
    
except FinancialDataError as e:
    # Handle financial data specific errors
    print(f"Financial data error: {e}")
    # Attempt to recover or provide partial analysis
    
except DocumentFormatError as e:
    # Handle document format issues
    print(f"Document format error: {e}")
    # Attempt to reformat or use alternative parsing
    
except APIError as e:
    # Handle API-related errors
    print(f"API error: {e}")
    # Implement retry logic or fallback
    
except Exception as e:
    # Handle unexpected errors
    print(f"Unexpected error: {e}")
    # Log error and provide graceful degradation
```

### 5. Financial Context Preservation
- **Metric Tracking**: Maintains context of financial metrics across queries
- **Historical Comparison**: Preserves historical financial data for trend analysis
- **Industry Context**: Maintains industry-specific financial benchmarks
- **Document Relationships**: Tracks relationships between related financial documents

### 6. Performance Optimization
- **Caching**: Implements intelligent caching of financial data
- **Batch Processing**: Optimizes processing of multiple financial documents
- **Parallel Analysis**: Concurrent analysis of related financial metrics
- **Resource Management**: Efficient memory and CPU usage for large documents

### 7. Security and Compliance
- **Data Encryption**: Secure handling of sensitive financial data
- **Access Control**: Role-based access to financial analysis features
- **Audit Logging**: Comprehensive logging of financial analysis operations
- **Compliance Checks**: Validation against financial reporting standards

### 8. Financial Analysis Quality Control
```python
# Example of quality control checks
def analyze_financial_statement(document):
    try:
        # Initial analysis
        analysis = mrag.ask("Analyze financial metrics")
        
        # Quality checks
        if not validate_financial_metrics(analysis):
            raise FinancialDataError("Invalid financial metrics detected")
            
        if not check_consistency(analysis):
            raise ConsistencyError("Inconsistent financial data")
            
        # Additional validation
        validate_against_industry_standards(analysis)
        check_for_anomalies(analysis)
        
        return analysis
        
    except FinancialAnalysisError as e:
        # Handle analysis-specific errors
        log_error(e)
        return partial_analysis_with_warnings()
```

### 9. Monitoring and Reporting
- **Performance Metrics**: Tracks analysis speed and accuracy
- **Error Rates**: Monitors and reports error frequencies
- **Quality Metrics**: Measures analysis quality and completeness
- **Usage Statistics**: Tracks feature usage and performance

### 10. Continuous Improvement
- **Error Pattern Analysis**: Identifies common error patterns
- **Automated Testing**: Regular testing of financial analysis capabilities
- **Performance Optimization**: Continuous optimization of analysis algorithms
- **Feature Enhancement**: Regular updates based on user feedback

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 