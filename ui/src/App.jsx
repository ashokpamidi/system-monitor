import { useEffect, useState} from 'react';
import axios from 'axios';
import './App.css';
import '../components/overall_summary.css';
import SummaryStat from '../components/overall_summary';
import wsTest from '../components/ws_test.jsx'

const API_URL = "http://127.0.0.1:8000"

function App() {
  const totalActiveProcesses = "1254"
  const overallSummary = wsTest();
  console.log(overallSummary)

  return (
    <>
      <div>
        <h1>Personal System Monitoring</h1>
      </div>

      <div className="summary_row">
        <SummaryStat label="Total Active Processes" value={overallSummary.total_active_processes}/>
        <SummaryStat label="Most Active Process" value={overallSummary.app_name}/>
        <SummaryStat label="Total Cursor Movement" value={overallSummary.cursor_position}/>
        <SummaryStat label="Session Duration" value={overallSummary.timestamp}/>
      </div>

    </>
  );
}

export default App;
