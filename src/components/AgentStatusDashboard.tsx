import React, { useCallback, useEffect, useState } from 'react';

interface AgentStatus {
  agent: string;
  message: string;
  status: 'Queued' | 'Running' | 'Completed' | 'Failed';
  progress?: number;
  timestamp?: string;
  started_at?: string;
  completed_at?: string;
}

const columns: Record<AgentStatus['status'], string> = {
  Queued: 'Queued',
  Running: 'Running',
  Completed: 'Completed',
  Failed: 'Failed',
};

const AgentStatusDashboard: React.FC = () => {
  const [statuses, setStatuses] = useState<AgentStatus[]>([]);

  const fetchHistory = useCallback(async () => {
    try {
      const resp = await fetch('/api/collaboration/agent_status?limit=50');
      const data = await resp.json();
      setStatuses(data.updates || []);
    } catch (err) {
      console.error('Failed to fetch agent status history', err);
    }
  }, []);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  useEffect(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const ws = new WebSocket(`${protocol}://${window.location.host}/ws`);

    ws.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        if (payload.event === 'agent_status_update') {
          setStatuses((prev) => [...prev.slice(-49), payload.data]);
        }
      } catch (err) {
        console.error('Invalid WebSocket message', err);
      }
    };

    return () => ws.close();
  }, []);

  const grouped: Record<string, AgentStatus[]> = statuses.reduce(
    (acc, item) => {
      (acc[item.status] ||= []).push(item);
      return acc;
    },
    { Queued: [], Running: [], Completed: [], Failed: [] } as Record<string, AgentStatus[]>
  );

  return (
    <div>
      <button onClick={fetchHistory}>Refresh</button>
      <div style={{ display: 'flex', gap: '1rem' }}>
        {Object.keys(columns).map((column) => (
          <div key={column} style={{ flex: 1 }}>
            <h3>{columns[column as AgentStatus['status']]}</h3>
            {grouped[column]?.map((item, idx) => (
              <div
                key={idx}
                style={{
                  border: '1px solid #ccc',
                  marginBottom: '0.5rem',
                  padding: '0.5rem',
                }}
              >
                <div><strong>{item.agent}</strong></div>
                <div>{item.message}</div>
                {item.progress !== undefined && <div>Progress: {item.progress}%</div>}
                {item.timestamp && <div>Updated: {new Date(item.timestamp).toLocaleString()}</div>}
                {item.started_at && <div>Started: {new Date(item.started_at).toLocaleString()}</div>}
                {item.completed_at && <div>Completed: {new Date(item.completed_at).toLocaleString()}</div>}
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
};

export default AgentStatusDashboard;
