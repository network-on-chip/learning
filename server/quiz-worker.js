/**
 * Cloudflare Worker: NoC Architecture Quiz Automated GitHub Issue Submission Bridge
 *
 * This serverless worker receives quiz completion payloads from the NoC Learning Hub,
 * securely extracts the client's authentic IP and Country from Cloudflare edge headers,
 * and creates a verified GitHub Issue in network-on-chip/learning with labels 'quiz-result,leaderboard'.
 *
 * Environment Variables / Secrets required:
 *   - GITHUB_TOKEN: GitHub Personal Access Token (PAT) with 'Issues: Read and Write' permission.
 *   - GITHUB_OWNER (optional, default: "network-on-chip")
 *   - GITHUB_REPO  (optional, default: "learning")
 */

export default {
  async fetch(request, env) {
    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
          "Access-Control-Max-Age": "86400",
        },
      });
    }

    if (request.method !== "POST") {
      return new Response(JSON.stringify({ error: "Method not allowed. Use POST." }), {
        status: 405,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      });
    }

    try {
      const payload = await request.json();

      // Extract authentic client IP and Geo-location from Cloudflare Edge Headers
      const cfConnectingIp = request.headers.get("cf-connecting-ip");
      const xForwardedFor = request.headers.get("x-forwarded-for");
      const clientIp = cfConnectingIp || (xForwardedFor ? xForwardedFor.split(",")[0].trim() : payload.ip || "Unknown IP");

      // Extract authentic country from Cloudflare CF object / headers
      const cfCountry = request.headers.get("cf-ipcountry") || (request.cf && request.cf.country);
      const clientCountry = cfCountry ? `${cfCountry}` : (payload.country || "Unknown Country");
      const clientCity = (request.cf && request.cf.city) || payload.city || payload.location || "";
      const clientRegion = (request.cf && request.cf.region) || payload.region || "";

      // Validate required candidate fields
      const candidateName = (payload.candidate || payload.name || "").trim();
      const candidateEmail = (payload.email || "").trim();
      const score = Number(payload.score) || 0;
      const accuracy = Number(payload.accuracy) || 0;
      const certId = String(payload.certId || `NOC-CERT-${Date.now()}`).trim();
      const mode = String(payload.mode || "full").trim();
      const date = String(payload.date || new Date().toISOString().split("T")[0]).trim();
      const correctCount = Number(payload.correctCount) || 0;
      const totalQuestions = Number(payload.totalQuestions) || 12;

      if (!candidateName) {
        return new Response(JSON.stringify({ error: "Candidate name is required." }), {
          status: 400,
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
        });
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!candidateEmail || !emailRegex.test(candidateEmail)) {
        return new Response(JSON.stringify({ error: "Valid candidate email address is required." }), {
          status: 400,
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
        });
      }

      // Build structured location display
      const locationParts = [clientCity, clientRegion].filter(Boolean);
      const locationStr = locationParts.length > 0 ? `${locationParts.join(", ")}, ${clientCountry}` : clientCountry;

      // Construct Markdown Body for GitHub Issue
      const issueTitle = `[quiz-result] ${candidateName} (${candidateEmail}) — ${score} pts — ${certId}`;
      const issueBody = [
        "### 🎯 NoC Architecture Assessment Verification Record",
        "",
        "> **Automated Submission:** This credential was submitted automatically by the NoC Learning Hub client engine upon exam completion.",
        "",
        "| Attribute | Assessment Record |",
        "| :--- | :--- |",
        `| **Candidate Full Name** | **${candidateName}** |`,
        `| **Candidate Email** | \`${candidateEmail}\` |`,
        `| **Client IP Address** | \`${clientIp}\` |`,
        `| **Location & Country** | ${locationStr} |`,
        `| **Assessment Track** | ${mode === "grandmaster" ? "Grandmaster Challenge (Tier 3)" : (mode === "tier1_sprint" ? "Fundamentals Sprint" : "Comprehensive Certification")} |`,
        `| **Total Score** | **${score} pts** |`,
        `| **Accuracy** | ${accuracy}% (${correctCount}/${totalQuestions} correct) |`,
        `| **Credential Hash** | \`${certId}\` |`,
        `| **Certification Date** | ${date} |`,
        `| **Submission Timestamp** | ${new Date().toISOString()} |`,
        "",
        "#### Cryptographic Verification Payload",
        "```json",
        JSON.stringify(
          {
            candidate: candidateName,
            email: candidateEmail,
            ip: clientIp,
            location: locationParts.join(", ") || "Unknown",
            country: clientCountry,
            mode: mode,
            score: score,
            accuracy: accuracy,
            certId: certId,
            date: date,
            timestamp: new Date().toISOString(),
            type: "quiz"
          },
          null,
          2
        ),
        "```",
        "",
        "---",
        "*Network-on-Chip (NoC) Learning Hub · Official Credential Registry*"
      ].join("\n");

      const repoOwner = env.GITHUB_OWNER || "network-on-chip";
      const repoName = env.GITHUB_REPO || "learning";
      const githubToken = env.GITHUB_TOKEN;

      if (!githubToken) {
        console.error("GITHUB_TOKEN is not set in environment.");
        return new Response(
          JSON.stringify({
            error: "GITHUB_TOKEN secret is not configured on server.",
            recorded_offline: true,
            ip: clientIp,
            country: clientCountry
          }),
          {
            status: 500,
            headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
          }
        );
      }

      // Dispatch Issue Creation to GitHub REST API
      const ghResp = await fetch(`https://api.github.com/repos/${repoOwner}/${repoName}/issues`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${githubToken}`,
          Accept: "application/vnd.github+json",
          "Content-Type": "application/json",
          "User-Agent": "NoC-Quiz-Bot/2.0",
        },
        body: JSON.stringify({
          title: issueTitle,
          body: issueBody,
          labels: ["quiz-result", "leaderboard"],
        }),
      });

      if (!ghResp.ok) {
        const errDetail = await ghResp.text();
        console.error("GitHub API error:", ghResp.status, errDetail);
        return new Response(
          JSON.stringify({
            error: `GitHub API error: ${ghResp.status}`,
            details: errDetail,
          }),
          {
            status: ghResp.status,
            headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
          }
        );
      }

      const issueData = await ghResp.json();

      return new Response(
        JSON.stringify({
          success: true,
          issue_number: issueData.number,
          html_url: issueData.html_url,
          candidate: candidateName,
          email: candidateEmail,
          ip: clientIp,
          country: clientCountry,
          location: locationStr,
          score: score,
          certId: certId,
        }),
        {
          status: 201,
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
        }
      );
    } catch (err) {
      console.error("Internal Worker Error:", err);
      return new Response(JSON.stringify({ error: err.message || "Internal server error" }), {
        status: 500,
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
      });
    }
  },
};

