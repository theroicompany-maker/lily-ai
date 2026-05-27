import React, { useState, useEffect, useRef } from 'react';
import './LiLy_Dashboard.css';

const LiLyDashboard = () => {
  const [systemStatus, setSystemStatus] = useState({
    core: true,
    realEstate: true,
    construction: true,
    memory: true,
    api: true,
    weather: true,
  });

  const [greeting, setGreeting] = useState('');
  const [currentTime, setCurrentTime] = useState(new Date());
  const [weather, setWeather] = useState({
    location: 'Dallas, TX',
    temp: 75,
    condition: 'Overcast',
    wind: 5,
    humidity: 87,
    forecast: [
      { day: 'Thu', icon: '⛈️', high: 83, low: 68 },
      { day: 'Fri', icon: '🌧️', high: 92, low: 72 },
      { day: 'Sat', icon: '☁️', high: 94, low: 76 },
    ],
  });

  const [schedule, setSchedule] = useState([
    { time: '9:00 AM', title: 'Deal Review', description: 'Casa Del Sol underwriting' },
    { time: '11:30 AM', title: 'Broker Call', description: 'DFW market update' },
    { time: '2:00 PM', title: 'Site Walkthrough', description: 'Main St Renovation' },
    { time: '4:00 PM', title: 'Offer Deadline', description: 'Submit LOI — Weatherford' },
  ]);

  const [briefing, setBriefing] = useState({
    dealsAnalyzed: 0,
    rfisGenerated: 0,
    emailsDrafted: 0,
    notifications: 2,
  });

  const [activity, setActivity] = useState([
    { time: '02:19 PM', message: 'Market search complete — 8 properties found matching your buy box' },
    { time: '02:18 PM', message: 'Morning market search starting — scanning DFW listings...' },
    { time: '02:18 PM', message: 'Weather loaded — Dallas TX' },
    { time: '02:18 PM', message: 'Good afternoon, Edward. All systems operational. Click the microphone button to activate voice.' },
    { time: '02:18 PM', message: 'Weather Feed verified' },
    { time: '02:18 PM', message: 'API Connection verified' },
    { time: '02:18 PM', message: 'Memory System verified' },
    { time: '02:18 PM', message: 'Construction Module verified' },
    { time: '02:18 PM', message: 'Real Estate Module verified' },
    { time: '02:18 PM', message: 'Core Brain verified' },
    { time: '02:18 PM', message: 'Memory loaded — 0 deals, 0 projects, 1 log items' },
    { time: '02:18 PM', message: 'LILY initialized — all modules loaded' },
    { time: 'Just now', message: 'Deal framework active — DFW buy box loaded' },
  ]);

  const [commandInput, setCommandInput] = useState('');
  const [voiceActive, setVoiceActive] = useState(false);
  const [currentModule, setCurrentModule] = useState('dashboard');
  const [showSettings, setShowSettings] = useState(false);
  const inputRef = useRef(null);

  // Update greeting based on time
  useEffect(() => {
    const hour = new Date().getHours();
    let greet = 'Good ';
    if (hour < 12) greet += 'morning';
    else if (hour < 18) greet += 'afternoon';
    else greet += 'evening';
    setGreeting(greet);
  }, []);

  // Update time
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const handleCommandSubmit = (e) => {
    e.preventDefault();
    if (!commandInput.trim()) return;

    // Log the command
    const newActivity = {
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      message: `User: ${commandInput}`,
    };
    setActivity([newActivity, ...activity]);

    // Simulate Claude processing
    setTimeout(() => {
      setActivity(prev => [{
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        message: `Claude: Processing "${commandInput}"...`,
      }, ...prev]);
    }, 500);

    setCommandInput('');
    inputRef.current?.focus();
  };

  const toggleVoice = () => {
    setVoiceActive(!voiceActive);
    if (!voiceActive) {
      // Start listening
      console.log('Voice activated');
    }
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const formatDate = (date) => {
    return date.toLocaleDateString([], { weekday: 'short', month: 'short', day: 'numeric' });
  };

  return (
    <div className="lily-container">
      {/* Header */}
      <header className="lily-header">
        <div className="header-left">
          <div className="time-date">
            <div className="time">{formatTime(currentTime)}</div>
            <div className="date">{formatDate(currentTime)}</div>
          </div>
        </div>
        <div className="header-center">
          <h1 className="lily-title">LiLY</h1>
        </div>
        <div className="header-right">
          <div className="status-indicator">
            <span className="status-dot"></span>
            All Systems Operational
          </div>
          <button className="settings-btn" onClick={() => setShowSettings(!showSettings)}>
            ⚙
          </button>
        </div>
      </header>

      <div className="lily-main">
        {/* Sidebar */}
        <aside className="lily-sidebar">
          <div className="sidebar-branding">
            <div className="lily-logo">⬡</div>
            <span>LiLY</span>
          </div>

          <nav className="sidebar-nav">
            <button
              className={`nav-item ${currentModule === 'dashboard' ? 'active' : ''}`}
              onClick={() => setCurrentModule('dashboard')}
            >
              ⬡ Dashboard
            </button>
            <button
              className={`nav-item ${currentModule === 'realEstate' ? 'active' : ''}`}
              onClick={() => setCurrentModule('realEstate')}
            >
              🏢 Real Estate
            </button>
            <button
              className={`nav-item ${currentModule === 'propertyMgmt' ? 'active' : ''}`}
              onClick={() => setCurrentModule('propertyMgmt')}
            >
              🏠 Property Mgmt
            </button>
            <button
              className={`nav-item ${currentModule === 'construction' ? 'active' : ''}`}
              onClick={() => setCurrentModule('construction')}
            >
              🏗 Construction
            </button>
          </nav>

          {showSettings && (
            <div className="sidebar-settings">
              <h3>Settings</h3>
              <ul>
                <li>⚙ API Keys</li>
                <li>👤 Profile</li>
                <li>📍 Location</li>
                <li>🔔 Notifications</li>
              </ul>
            </div>
          )}
        </aside>

        {/* Main Content */}
        <main className="lily-content">
          {/* Top Section */}
          <section className="lily-top">
            <div className="system-status">
              <div className="status-header">
                ⬡ ALL SYSTEMS OPERATIONAL
              </div>
              <div className="user-greeting">
                {greeting}, Edward.
              </div>
              <div className="contextual-prompt">
                Markets are open. What are we working on?
              </div>
            </div>

            <div className="quick-cards">
              <div className="quick-card">
                <div className="card-icon">🔍</div>
                <div className="card-content">
                  <div className="card-number">8</div>
                  <div className="card-label">New Listings Found</div>
                </div>
              </div>
              <div className="quick-card">
                <div className="card-icon">📋</div>
                <div className="card-content">
                  <div className="card-number">1</div>
                  <div className="card-label">Open Submittals</div>
                </div>
              </div>
              <button className="quick-card-btn">V</button>
            </div>
          </section>

          {/* Main Grid */}
          <div className="lily-grid">
            {/* Left Column */}
            <div className="grid-left">
              {/* Morning Briefing */}
              <section className="briefing-section">
                <div className="section-header">
                  <span>⬡ MORNING BRIEFING</span>
                </div>
                <div className="briefing-stats">
                  <div className="stat">
                    <div className="stat-label">Deals Analyzed</div>
                    <div className="stat-value">{briefing.dealsAnalyzed}</div>
                    <div className="stat-period">Session</div>
                  </div>
                  <div className="stat">
                    <div className="stat-label">RFIs Generated</div>
                    <div className="stat-value">{briefing.rfisGenerated}</div>
                    <div className="stat-period">Session</div>
                  </div>
                  <div className="stat">
                    <div className="stat-label">Emails Drafted</div>
                    <div className="stat-value">{briefing.emailsDrafted}</div>
                    <div className="stat-period">Session</div>
                  </div>
                  <div className="stat">
                    <div className="stat-label">Notifications</div>
                    <div className="stat-value">{briefing.notifications}</div>
                    <div className="stat-period">Active</div>
                  </div>
                </div>
                <button className="briefing-button">⬡ Run Briefing</button>
              </section>

              {/* Activity Log */}
              <section className="activity-section">
                <div className="section-header">System Activity</div>
                <div className="activity-log">
                  {activity.slice(0, 8).map((item, idx) => (
                    <div key={idx} className="activity-item">
                      <span className="activity-time">{item.time}</span>
                      <span className="activity-message">{item.message}</span>
                    </div>
                  ))}
                </div>
              </section>
            </div>

            {/* Right Column */}
            <div className="grid-right">
              {/* Weather */}
              <section className="weather-section">
                <div className="section-header">Weather — {weather.location}</div>
                <div className="weather-current">
                  <div className="weather-icon">☁️</div>
                  <div className="weather-details">
                    <div className="weather-temp">{weather.temp}°F</div>
                    <div className="weather-condition">{weather.condition}</div>
                    <div className="weather-details-line">
                      <span>💨 {weather.wind} mph</span>
                      <span>💧 {weather.humidity}%</span>
                    </div>
                  </div>
                </div>
                <div className="weather-forecast">
                  {weather.forecast.map((day, idx) => (
                    <div key={idx} className="forecast-day">
                      <div className="forecast-day-name">{day.day}</div>
                      <div className="forecast-icon">{day.icon}</div>
                      <div className="forecast-temps">{day.high}°/{day.low}°</div>
                    </div>
                  ))}
                </div>
              </section>

              {/* Schedule */}
              <section className="schedule-section">
                <div className="section-header">Today's Schedule</div>
                <div className="schedule-list">
                  {schedule.map((event, idx) => (
                    <div key={idx} className="schedule-item">
                      <div className="schedule-time">{event.time}</div>
                      <div className="schedule-details">
                        <div className="schedule-title">{event.title}</div>
                        <div className="schedule-description">{event.description}</div>
                      </div>
                    </div>
                  ))}
                </div>
                <button className="schedule-add">+ Add Event</button>
              </section>
            </div>
          </div>
        </main>
      </div>

      {/* Command Bar (Bottom) */}
      <footer className="lily-footer">
        <form className="command-bar" onSubmit={handleCommandSubmit}>
          <div className="command-input-wrapper">
            <button
              type="button"
              className={`voice-btn ${voiceActive ? 'active' : ''}`}
              onClick={toggleVoice}
              title="Activate voice input"
            >
              🎤
            </button>
            <input
              ref={inputRef}
              type="text"
              className="command-input"
              placeholder={voiceActive ? 'Listening...' : 'Click 🎤 to activate'}
              value={commandInput}
              onChange={(e) => setCommandInput(e.target.value)}
            />
            <button type="submit" className="send-btn">
              SEND ↑
            </button>
          </div>
        </form>
      </footer>

      {/* Settings Modal */}
      {showSettings && (
        <div className="settings-modal" onClick={() => setShowSettings(false)}>
          <div className="settings-content" onClick={(e) => e.stopPropagation()}>
            <h2>⚙ Settings</h2>
            <div className="settings-grid">
              <div className="setting-item">
                <label>Core Brain</label>
                <div className={`toggle ${systemStatus.core ? 'on' : 'off'}`} />
              </div>
              <div className="setting-item">
                <label>Real Estate Module</label>
                <div className={`toggle ${systemStatus.realEstate ? 'on' : 'off'}`} />
              </div>
              <div className="setting-item">
                <label>Construction Module</label>
                <div className={`toggle ${systemStatus.construction ? 'on' : 'off'}`} />
              </div>
              <div className="setting-item">
                <label>Memory System</label>
                <div className={`toggle ${systemStatus.memory ? 'on' : 'off'}`} />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default LiLyDashboard;
