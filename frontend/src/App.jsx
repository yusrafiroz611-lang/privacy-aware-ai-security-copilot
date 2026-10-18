import { useState } from 'react'
import { analyzeRequest } from './api'
import './App.css'
function App() {
  const [analysisText, setAnalysisText] = useState('')
  const [analysisResult, setAnalysisResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  return (
    <div className="app">

      {/* Header */}
      <header className="header">
        <div>
          <h1>Privacy-Aware AI Security Copilot</h1>
          <p>Secure AI. Protected Data.</p>
        </div>

        <span className="system-status">
          ● System Protected
        </span>
      </header>

      <main>

        {/* Security Overview */}
       <section className="stats">
  <div className="card risk-card">
    <span className="card-label">RISK SCORE</span>

    <div className="card-main-value">
      {analysisResult
  ? (analysisResult.risk_score == null ? 'N/A' : `${Math.round(analysisResult.risk_score * 100)}%`)
  : '--'}
    </div>

    <span className="card-status">
      {analysisResult
        ? analysisResult.high_risk
          ? '● Elevated Risk'
          : '● Normal Risk'
        : '● Awaiting Analysis'}
    </span>
  </div>

  <div className="card decision-card">
    <span className="card-label">SECURITY DECISION</span>

    <div
      className={`card-main-value decision-value ${
        analysisResult ? analysisResult.decision.toLowerCase() : ''
      }`}
    >
      {analysisResult ? analysisResult.decision : '--'}
    </div>

    <span className="card-status">
      {analysisResult ? '● Policy Evaluation' : '● Awaiting Analysis'}
    </span>
  </div>

  <div className="card privacy-card">
    <span className="card-label">PRIVACY DETECTIONS</span>

    <div className="card-main-value">
      {analysisResult ? analysisResult.privacy_detections : '--'}
    </div>

    <span className="card-status">
      {analysisResult
        ? analysisResult.privacy_detections > 0
          ? '● Sensitive Data Found'
          : '● No Sensitive Data'
        : '● Awaiting Analysis'}
    </span>
  </div>

  <div className="card model-card">
    <span className="card-label">MODEL VERSION</span>

    <div className="card-main-value">
      {analysisResult ? analysisResult.model_version : '--'}
    </div>

    <span className="card-status">
      {analysisResult ? '● Active Model' : '● Awaiting Analysis'}
    </span>
  </div>
</section>

        {/* Security Analysis */}
        <section className="analysis-section">
  <div className="section-heading">
    <div>
      <span className="section-kicker">SECURITY PIPELINE</span>
      <h2>Analysis Flow</h2>
    </div>
    <span className="pipeline-status">● READY</span>
  </div>

  <div className="pipeline">
    <div className="pipeline-step">
      <span className="pipeline-number">01</span>
      <h3>Predict</h3>
      <p>Behavioral activity is evaluated for risk.</p>
    </div>

    <div className="pipeline-arrow">→</div>

    <div className="pipeline-step">
      <span className="pipeline-number">02</span>
      <h3>Protect</h3>
      <p>Sensitive information is detected and sanitized.</p>
    </div>

    <div className="pipeline-arrow">→</div>

    <div className="pipeline-step">
      <span className="pipeline-number">03</span>
      <h3>Explain</h3>
      <p>GenAI explains the detected security risk.</p>
    </div>

    <div className="pipeline-arrow">→</div>

    <div className="pipeline-step">
      <span className="pipeline-number">04</span>
      <h3>Validate</h3>
      <p>Generated output is checked for data leakage.</p>
    </div>

    <div className="pipeline-arrow">→</div>

    <div className="pipeline-step">
      <span className="pipeline-number">05</span>
      <h3>Decide</h3>
      <p>Policy determines Allow, Warn, or Block.</p>
    </div>

    <div className="pipeline-arrow">→</div>

    <div className="pipeline-step">
      <span className="pipeline-number">06</span>
      <h3>Record</h3>
      <p>The security decision is recorded for audit.</p>
    </div>
  </div>
</section>

                {/* Analysis Request */}
        <section className="request-section">
  <div className="section-heading">
    <div>
      <span className="section-kicker">SECURITY ANALYSIS</span>
      <h2>Analyze Request</h2>
    </div>
    <span className="request-status">● PROTECTED INPUT</span>
  </div>

  <div className="request-card">
    <label htmlFor="analysis-input">
      Security activity or request
    </label>

    <p className="input-description">
      Enter a synthetic security request for risk and privacy analysis.
    </p>

    <textarea
      id="analysis-input"
      placeholder="Example: User requested access to confidential customer records..."
      value={analysisText}
      onChange={(event) => setAnalysisText(event.target.value)}
    ></textarea>

    <div className="request-footer">
      <span className="input-hint">
        Sensitive information will be protected before AI processing.
      </span>

      <button
        className="analyze-button"
        onClick={async () => {
          setError('')
          setAnalysisResult(null)
          setLoading(true)

          let result

          try {
            result = await analyzeRequest(analysisText)
          } catch (error) {
            setLoading(false)
            setError('Unable to connect to the security analysis service.')
            return
          }

          setLoading(false)

          if (!result.success) {
            setError('Unable to analyze the request.')
            return
          }

         setError('')

if (!result.data) {
  setError('Security analysis returned no data.')
  return
}

setAnalysisResult(result.data)
        }}
        disabled={loading || !analysisText.trim()}
      >
        {loading ? 'Analyzing Security Request...' : 'Analyze Request →'}
      </button>
    </div>

    {error && (
  <div className="error-message">
    <strong>Analysis Failed</strong>
    <span>{error}</span>
  </div>
)}
  </div>
</section>
        {/* Privacy Findings & Decision Reason */}
       <section className="details-section">

  <div className="detail-card privacy-result-card">
    <div className="result-card-header">
      <div>
        <span className="section-kicker">PROTECT</span>
        <h2>Privacy Protection</h2>
      </div>

      <span className="result-badge">
        {analysisResult
          ? `${analysisResult.privacy_detections} DETECTED`
          : '--'}
      </span>
    </div>

    <h3>Detected Entities</h3>

    <div className="entity-list">
      {analysisResult?.privacy_findings?.length ? (
  analysisResult.privacy_findings.map((finding, index) => (
          <span className="entity-tag" key={index}>
            {finding}
          </span>
        ))
      ) : (
  <span className="empty-state">
    No privacy findings available.
  </span>
)}
    </div>

    <h3>Sanitized Preview</h3>

    <div className="sanitized-preview">
      {analysisResult
        ? analysisResult.sanitized_text
        : 'Sanitized request will appear here after analysis.'}
    </div>
  </div>

  <div className="detail-card decision-result-card">
    <div className="result-card-header">
      <div>
        <span className="section-kicker">DECISION</span>
        <h2>Security Decision</h2>
      </div>

      <span
        className={`decision-badge ${
  analysisResult?.decision
    ? analysisResult.decision.toLowerCase()
    : ''
}`}
      >
        {analysisResult ? analysisResult.decision : '--'}
      </span>
    </div>

    <h3>Decision Reason</h3>

    <p className="decision-description">
      {analysisResult
        ? analysisResult.decision_reason
        : 'The security decision will appear here after analysis.'}
    </p>

    <div className="decision-meta">
      <div>
        <span>Risk Level</span>
        <strong>
          {analysisResult
            ? analysisResult.high_risk
              ? 'HIGH'
              : 'NORMAL'
            : '--'}
        </strong>
      </div>

      <div>
        <span>Recommendation</span>
        <strong>
          {analysisResult
            ? analysisResult.recommendation
            : '--'}
        </strong>
      </div>
    </div>
  </div>

</section>


{/* GenAI Explanation */}
<section className="genai-section">
  <div className="section-heading">
    <div>
      <span className="section-kicker">EXPLAIN</span>
      <h2>GenAI Explanation</h2>
    </div>

    <span className="ai-badge">AI ANALYSIS</span>
  </div>

  <div className="genai-card">
    <h3>Risk Explanation</h3>

    <p className="genai-explanation">
      {analysisResult
        ? analysisResult.genai_explanation
        : 'No AI-generated explanation available.'}
    </p>

    <div className="recommendation-row">
      <span>AI Recommendation</span>

      <p
        className={`recommendation-value ${
  analysisResult?.recommendation
    ? analysisResult.recommendation.toLowerCase()
    : ''
}`}
      >
        {analysisResult
          ? analysisResult.recommendation
          : '--'}
      </p>
    </div>
  </div>
</section>


        {/* Audit History */}

        {/* AI Response Validation */}

<section className="validation-section">
  <div className="section-heading">
    <div>
      <span className="section-kicker">VALIDATE</span>
      <h2>AI Response Validation</h2>
    </div>

    <span className="validation-badge">
      {analysisResult
        ? analysisResult.validation_status
        : 'AWAITING'}
    </span>
  </div>

  <div className="validation-card">
    <div className="validation-main">
      <div>
        <span className="validation-label">VALIDATION STATUS</span>

        <p
          className={`validation-status ${
            analysisResult?.validation_status?.toLowerCase() || ''
          }`}
        >
          {analysisResult
            ? analysisResult.validation_status
            : '--'}
        </p>
      </div>

      <div>
        <span className="validation-label">LEAKAGE CHECK</span>

        <p className="validation-check">
          {analysisResult
            ? analysisResult.validation_status === 'PASSED'
              ? 'No sensitive-data leakage detected'
              : 'Potential sensitive-data leakage detected'
            : 'Awaiting AI response validation'}
        </p>
      </div>
    </div>

    <div className="validation-reason">
      <span className="validation-label">VALIDATION REASON</span>

      <p>
        {analysisResult
          ? analysisResult.validation_reason
          : 'The generated AI response will be checked for sensitive-data leakage before delivery.'}
      </p>
    </div>
  </div>
</section>
<section className="audit-section">
  <div className="section-heading">
    <div>
      <span className="section-kicker">RECORD</span>
      <h2>Audit History</h2>
    </div>

    <span className="audit-badge">
      {analysisResult ? 'RECORDED' : 'AWAITING'}
    </span>
  </div>

  <div className="audit-card">
    {analysisResult ? (
      <>
        <div className="audit-header">
          <div>
            <span className="audit-label">SECURITY ANALYSIS RECORD</span>
            <h3>Audit Entry</h3>
          </div>

          <span className="audit-id">
            {analysisResult.audit_id}
          </span>
        </div>

        <div className="audit-record">
          <div className="audit-item">
            <span>Timestamp</span>
            <strong>{analysisResult.timestamp}</strong>
          </div>

          <div className="audit-item">
            <span>Risk Score</span>
            <strong>
              {analysisResult.risk_score == null ? 'N/A' : `${Math.round(analysisResult.risk_score * 100)}%`}
            </strong>
          </div>

          <div className="audit-item">
            <span>Final Decision</span>
            <strong>{analysisResult.decision}</strong>
          </div>

          <div className="audit-item">
            <span>Model Version</span>
            <strong>{analysisResult.model_version}</strong>
          </div>
        </div>
      </>
    ) : (
      <div className="audit-empty">
        <span className="audit-empty-icon">○</span>

        <div>
          <h3>No audit records yet</h3>
          <p>
            A security audit record will be created after a request
            completes the analysis pipeline.
          </p>
        </div>
      </div>
    )}
  </div>
</section>
      </main>

    </div>
  )
}

export default App