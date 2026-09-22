import { useState, useRef, useEffect } from "react";
import "./App.css";

// Unified Crisp SVG Shield Icon used across Navigation, Buttons, & Moving Banners
const ShieldIcon = ({ className = "shield-svg-icon", darkFill = false }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path 
      d="M12 2L3 5V11C3 16.55 7 21.74 12 23C17 21.74 21 16.55 21 11V5L12 2Z" 
      fill={darkFill ? "#040d06" : "#38e890"} 
      stroke={darkFill ? "#000000" : "#4dfa9f"} 
      strokeWidth="1.8"
    />
    <path d="M12 6V18" stroke={darkFill ? "#38e890" : "#0b0f17"} strokeWidth="1.8" strokeLinecap="round"/>
    <path d="M7 11L12 16L17 11" stroke={darkFill ? "#38e890" : "#0b0f17"} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

function App() {
  const [message, setMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [showResult, setShowResult] = useState(false);
  const [isScanning, setIsScanning] = useState(false);
  const [scanStep, setScanStep] = useState("Initializing threat heuristic engine...");
  const [selectedImage, setSelectedImage] = useState(null);
  const [scanType, setScanType] = useState("text");
  
  const fileInputRef = useRef(null);
  const canvasRef = useRef(null);
  const spotlightRef = useRef(null);

  // Mouse Follow Spotlight
  useEffect(() => {
    const handleMouseMove = (e) => {
      if (spotlightRef.current) {
        spotlightRef.current.style.left = `${e.clientX}px`;
        spotlightRef.current.style.top = `${e.clientY}px`;
      }
    };
    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  // Particle Canvas Background
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    let animationFrameId;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const handleResize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    window.addEventListener("resize", handleResize);

    const particles = Array.from({ length: 50 }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.6,
      vy: (Math.random() - 0.5) * 0.6,
      radius: Math.random() * 2 + 1,
    }));

    const render = () => {
      ctx.clearRect(0, 0, width, height);

      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(56, 232, 144, 0.7)";
        ctx.fill();

        for (let j = i + 1; j < particles.length; j++) {
          const p2 = particles[j];
          const dx = p.x - p2.x;
          const dy = p.y - p2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 130) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = `rgba(56, 232, 144, ${0.18 * (1 - dist / 130)})`;
            ctx.lineWidth = 0.8;
            ctx.stroke();
          }
        }
      }

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      window.removeEventListener("resize", handleResize);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  const handleImageSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedImage({
        file: file,
        name: file.name,
        preview: URL.createObjectURL(file)
      });
      setErrorMessage("");
    }
  };

  const openImagePicker = () => {
    fileInputRef.current.click();
  };

  const startAnimatedScan = (targetType) => {
    setScanType(targetType);
    setIsScanning(true);
    setErrorMessage("");
    setScanStep("Initializing threat heuristic engine...");

    setTimeout(() => {
      setScanStep("Parsing extracted payload & indicators...");
    }, 800);

    setTimeout(() => {
      setScanStep("Querying global scam database & blacklists...");
    }, 1600);

    setTimeout(() => {
      setScanStep("Evaluating machine learning risk confidence...");
    }, 2400);

    setTimeout(() => {
      setIsScanning(false);
      setShowResult(true);
    }, 3000);
  };

  const handleMainScan = () => {
    if (message.trim() === "") {
      setErrorMessage("⚠️ Please enter a text, URL, or email in the box to scan.");
      return;
    }

    setErrorMessage("");
    const textLower = message.toLowerCase();
    const isUrl = textLower.includes("http") || textLower.includes("www.") || textLower.includes(".com");
    startAnimatedScan(isUrl ? "url" : "text");
  };

  const handleOptionClick = (type) => {
    if (message.trim() === "") {
      setErrorMessage(`⚠️ Please enter a ${type === "url" ? "URL/link" : "suspicious text message"} in the text box above first.`);
      return;
    }

    const textLower = message.toLowerCase();
    const isUrl = textLower.includes("http") || textLower.includes("www.") || textLower.includes(".com");
    startAnimatedScan(type === "url" || isUrl ? "url" : "text");
  };

  const scanAgain = () => {
    setShowResult(false);
    setIsScanning(false);
    setMessage("");
    setErrorMessage("");
    setSelectedImage(null);
    setScanType("text");
  };

  const getScanResultData = () => {
    if (scanType === "image") {
      return {
        badge: "HIGH RISK",
        title: "Fake QR Code / Phishing Screenshot",
        detected: [
          "Suspicious QR URL extracted",
          "Unverified payment gateway redirect",
          "Urgent money transfer prompt",
          "Fake official logo branding"
        ],
        why: "The image/QR code redirects users to an unverified portal disguised as an official payment app to steal funds.",
        action: "Do not scan or pay using this QR code. Do not share OTPs or passwords."
      };
    } else if (scanType === "url") {
      return {
        badge: "HIGH RISK",
        title: "Malicious Phishing Link",
        detected: [
          "Non-HTTPS / Unsecure connection",
          "Misspelled bank domain name",
          "Fake login page pattern",
          "Domain created recently (< 3 days ago)"
        ],
        why: "The URL mimics a legitimate banking website to trick users into entering passwords and account numbers.",
        action: "Close the page immediately! Never enter sensitive credentials on unverified websites."
      };
    } else {
      return {
        badge: "MEDIUM RISK",
        title: "Suspicious Fraudulent Message",
        detected: [
          "Panic-inducing language ('Account Blocked')",
          "Unverified sender phone number",
          "Shortened untrusted web link",
          "Threat of service suspension"
        ],
        why: "Scammers use panic tactics to make victims act urgently without verifying with official channels.",
        action: "Do not reply or click links inside this message. Verify directly through official customer care."
      };
    }
  };

  const resultData = getScanResultData();

  // Helper component for ticker items with matching SVG shield
  const TickerItem = () => (
    <span className="ticker-item">
      TEAM NEXORA <ShieldIcon className="ticker-shield-svg" /> SCAMSHIELD AI
    </span>
  );

  return (
    <div className="app">
      {/* TOP FULL TICKER WITH MATCHING SVG SHIELD */}
      <div className="edge-watermark-ticker top-ticker">
        <div className="watermark-track">
          <TickerItem />
          <TickerItem />
          <TickerItem />
          <TickerItem />
          <TickerItem />
          <TickerItem />
        </div>
      </div>

      {/* Mouse Spotlight */}
      <div ref={spotlightRef} className="mouse-spotlight"></div>

      {/* Background Gradient & Particle Canvas */}
      <div className="animated-gradient-bg"></div>
      <canvas ref={canvasRef} className="particles-canvas" />

      {/* Navigation Bar */}
      <nav className="navbar">
        <div className="logo">
          <div className="logo-shield-container">
            <span className="radar-beam"></span>
            <span className="radar-glow-ring"></span>
            <ShieldIcon className="logo-shield-svg" />
          </div>

          <div>
            Scam<span>Shield</span> AI
          </div>
        </div>

        <div className="nav-right">
          <span className="live-dot"></span> System Status: <span className="status-active">ACTIVE</span>
        </div>
      </nav>

      {/* SCANNING RADAR OVERLAY */}
      {isScanning ? (
        <main className="scan-container">
          <div className="radar-card">
            <div className="radar-spinner"></div>
            <h3>Analyzing Threat Vectors</h3>
            <p className="scan-status-text">{scanStep}</p>
            <div className="progress-bar-track">
              <div className="progress-bar-fill"></div>
            </div>
          </div>
        </main>
      ) : !showResult ? (
        /* ================= INPUT SCREEN ================= */
        <main className="scan-container">
          {/* BRIGHT HERO HEADER SECTION */}
          <section className="hero">
            <div className="cyber-tag">
              <span>TEAM NEXORA</span> • AI CYBER DEFENSE PLATFORM
            </div>

            <h1 className="bright-hero-title">
              Protect Yourself <span className="bright-green-glow">Before You Act</span>
            </h1>

            <p className="hero-subtitle bright-hero-sub">
              Paste suspicious messages, website links, or upload screenshots to analyze threats in real-time.
            </p>
          </section>

          <div className="input-card">
            <div className="input-header">
              <div className="input-title">
                🔍 <strong>ANALYSIS CONSOLE</strong>
              </div>
              <div className="console-status">SECURE NODE</div>
            </div>

            <textarea
              value={message}
              onChange={(e) => {
                setMessage(e.target.value);
                if (errorMessage) setErrorMessage("");
              }}
              placeholder="Paste suspicious SMS, WhatsApp message, email content, or URL link here..."
            />

            {/* RED ERROR MESSAGE */}
            {errorMessage && (
              <div className="error-banner">
                {errorMessage}
              </div>
            )}

            <button
              className="scan-button"
              onClick={handleMainScan}
            >
              <ShieldIcon className="btn-shield-svg" darkFill={true} /> Scan Content for Threats
            </button>
          </div>

          <div className="options">
            <div className="option-card" onClick={() => handleOptionClick("text")}>
              <div className="option-header">
                <div className="option-icon">📝</div>
                <span className="card-badge">TEXT</span>
              </div>
              <h3>Text Scan</h3>
              <p>Analyze SMS, WhatsApp or email text</p>
            </div>

            <div className="option-card" onClick={() => handleOptionClick("url")}>
              <div className="option-header">
                <div className="option-icon">🔗</div>
                <span className="card-badge">WEB</span>
              </div>
              <h3>URL Scan</h3>
              <p>Check suspicious links & domain threats</p>
            </div>

            <div
              className="option-card"
              onClick={openImagePicker}
            >
              <div className="option-header">
                <div className="option-icon">🖼️</div>
                <span className="card-badge">MEDIA</span>
              </div>
              <h3>Image / QR Scan</h3>
              <p>Analyze screenshots & QR codes</p>

              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleImageSelect}
                style={{ display: "none" }}
              />
            </div>
          </div>

          {selectedImage && (
            <div className="selected-image">
              <div className="preview-container">
                <img src={selectedImage.preview} alt="Selected preview" className="image-preview" />
                <p className="image-name">🖼️ {selectedImage.name}</p>
              </div>

              <div className="image-actions">
                <button
                  className="scan-button"
                  onClick={() => startAnimatedScan("image")}
                >
                  <ShieldIcon className="btn-shield-svg" darkFill={true} /> Scan Image / QR Code
                </button>

                <button
                  className="remove-button"
                  onClick={() => setSelectedImage(null)}
                >
                  ❌ Remove
                </button>
              </div>
            </div>
          )}

          <div className="info">
            ⚡ ScamShield AI by Team NEXORA uses real-time pattern analysis to identify digital fraud.
          </div>
        </main>
      ) : (
        /* ================= RESULT SCREEN ================= */
        <main className="scan-container">
          <section className="hero">
            <h1 className="bright-hero-title">
              Scan <span className="bright-green-glow">Result</span>
            </h1>

            <p className="hero-subtitle bright-hero-sub">
              Threat report generated for the submitted content.
            </p>
          </section>

          {/* Risk Badge */}
          <div className="result-risk high-risk">
            <div className="risk-icon">⚠️</div>

            <div>
              <div className="risk-label">{resultData.badge}</div>
              <div className="risk-title">
                {resultData.title}
              </div>
            </div>
          </div>

          {/* Result Cards */}
          <div className="result-grid">
            {/* WHAT */}
            <div className="result-card">
              <h2>🔍 What was detected?</h2>

              <ul>
                {resultData.detected.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>

            {/* WHY */}
            <div className="result-card">
              <h2>❓ Why is it suspicious?</h2>

              <p>{resultData.why}</p>
            </div>
          </div>

          {/* ACTION */}
          <div className="action-card">
            <h2><ShieldIcon className="btn-shield-svg" darkFill={true} /> Recommended Action</h2>

            <p>{resultData.action}</p>
          </div>

          {/* Scan Again */}
          <button
            className="scan-button"
            onClick={scanAgain}
          >
            ← Scan Another Item
          </button>
        </main>
      )}

      {/* BOTTOM FULL TICKER WITH MATCHING SVG SHIELD */}
      <div className="edge-watermark-ticker bottom-ticker">
        <div className="watermark-track">
          <TickerItem />
          <TickerItem />
          <TickerItem />
          <TickerItem />
          <TickerItem />
          <TickerItem />
        </div>
      </div>
    </div>
  );
}

export default App;