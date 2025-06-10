import React, { useEffect, useState } from 'react';


// useEffect
function wsTest() {
  const [overallSummary, setOverallSummary] = useState({'id': "",
                                                        'timestamp': "",
                                                        'total_active_processes': "",
                                                        'app_name': "",
                                                        'cursor_position': ""});

  useEffect(() => {
    const ws = new WebSocket('ws://127.0.0.1:8000/ws_test');
    
    ws.onmessage = (event) => {
      setOverallSummary(JSON.parse(event.data));
    };
    
    ws.onclose = () => {
      console.log('ws connection closed')
    };
  }, []);
  
  return overallSummary;
};

export default wsTest