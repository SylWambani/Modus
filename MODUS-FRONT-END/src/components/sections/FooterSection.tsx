const FooterSection = () => {
  return (
    <footer
      style={{
        backgroundColor: "#0f172a",
        color: "#e2e8f0",
        padding: "2rem 1rem",
      }}
    >
      <div
        style={{
          maxWidth: "1100px",
          margin: "0 auto",
          display: "grid",
          gap: "1.5rem",
          gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
          alignItems: "start",
        }}
      >
        <div>
          <h2 style={{ margin: 0, fontSize: "1.25rem", fontWeight: 700 }}>
            Modus ERP
          </h2>
          <p
            style={{
              margin: "0.75rem 0 0",
              lineHeight: 1.75,
              color: "#cbd5e1",
            }}
          >
            A fast, professional mini-ERP experience built to keep teams
            aligned, informed, and moving with confidence.
          </p>
        </div>

        <div>
          <h3 style={{ margin: 0, fontSize: "1rem", fontWeight: 600 }}>
            Contact
          </h3>
          <p style={{ margin: "0.75rem 0 0", lineHeight: 1.75 }}>
            +254 768 588 144
            <br />
            +254 734 987 826
          </p>
          <p style={{ margin: "0.75rem 0 0", lineHeight: 1.75 }}>
            <a
              href="mailto:wambanisylvia2@gmail.com"
              style={{ color: "#60a5fa", textDecoration: "none" }}
            >
              wambanisylvia2@gmail.com
            </a>
          </p>
        </div>

        <div>
          <h3 style={{ margin: 0, fontSize: "1rem", fontWeight: 600 }}>Info</h3>
          <p style={{ margin: "0.75rem 0 0", lineHeight: 1.75 }}>Version 1.0</p>
          <p style={{ margin: "0.75rem 0 0", lineHeight: 1.75 }}>
            Crafted with care by Sylvia Wambani.
          </p>
        </div>

        <div>
          <h3 style={{ margin: 0, fontSize: "1rem", fontWeight: 600 }}>
            Social
          </h3>
          <p style={{ margin: "0.75rem 0 0", lineHeight: 1.75 }}>
            <a
              href="https://linkedin.com/in/sylvia-wambani"
              target="_blank"
              rel="noreferrer"
              style={{ color: "#60a5fa", textDecoration: "none" }}
            >
              LinkedIn / Sylvia Wambani
            </a>
          </p>
          <p style={{ margin: "0.5rem 0 0", lineHeight: 1.75 }}>
            <a
              href="https://twitter.com/sylvia_wambani"
              target="_blank"
              rel="noreferrer"
              style={{ color: "#60a5fa", textDecoration: "none" }}
            >
              Twitter / @sylvia_wambani
            </a>
          </p>
        </div>
      </div>

      <div
        style={{
          marginTop: "1.75rem",
          borderTop: "1px solid rgba(226, 232, 240, 0.12)",
          paddingTop: "1rem",
          textAlign: "center",
          color: "#94a3b8",
          fontSize: "0.95rem",
        }}
      >
        © {new Date().getFullYear()} Modus ERP. All rights reserved.
      </div>
    </footer>
  );
};

export default FooterSection;
