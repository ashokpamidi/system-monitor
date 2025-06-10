import React from 'react';
import './overall_summary.css'
function SummaryStat(summary_props) {

  return (
    <div>
        <div>
          <div className="summary_stat_text">
              <h3>{summary_props.label}</h3>
          </div>
          <div className="summary_stat">
              <h1>{summary_props.value}</h1> 
          </div>
        </div>
    </div>
  )
}

export default SummaryStat