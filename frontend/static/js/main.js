/**
 * MedShield-X — Global JavaScript (main.js)
 * Handles: Theme toggle, Sidebar collapse, Auth guard,
 *          Doctor profile population, Logout, Activity logging
 */

document.addEventListener("DOMContentLoaded", function () {

    // =====================================================================
    // 1. THEME TOGGLE
    //    Persists user preference; defaults to 'light' (enterprise theme)
    // =====================================================================
    const themeBtn  = document.getElementById("theme-toggle-btn");
    const themeIcon = document.getElementById("theme-toggle-icon");

    function applyThemeIcon(theme) {
        if (!themeIcon) return;
        themeIcon.className = (theme === "dark")
            ? "fa-solid fa-moon"
            : "fa-solid fa-sun";
    }

    // Apply saved or default theme on load
    const savedTheme = localStorage.getItem("medshield_theme") || "light";
    applyThemeIcon(savedTheme);

    if (themeBtn) {
        themeBtn.addEventListener("click", () => {
            const current = document.documentElement.getAttribute("data-theme") || "light";
            const next    = current === "dark" ? "light" : "dark";
            document.documentElement.setAttribute("data-theme", next);
            localStorage.setItem("medshield_theme", next);
            applyThemeIcon(next);

            // Notify page scripts that theme changed (for Chart.js redraws)
            document.dispatchEvent(new CustomEvent("medshield:themechange", { detail: { theme: next } }));
        });
    }


    // =====================================================================
    // 2. SIDEBAR — Collapse / Expand (desktop only)
    // =====================================================================
    const sidebar           = document.getElementById("sidebar");
    const mainContent       = document.getElementById("main-content");
    const collapseBtn       = document.getElementById("sidebar-collapse-btn");
    const toggleIcon        = document.getElementById("toggle-icon");

    // Restore persisted collapse state
    const sidebarCollapsed = localStorage.getItem("medshield_sidebar_collapsed") === "true";
    if (sidebarCollapsed && sidebar && mainContent && window.innerWidth >= 992) {
        sidebar.classList.add("collapsed");
        mainContent.classList.add("sidebar-collapsed");
        if (toggleIcon) toggleIcon.className = "fa-solid fa-chevron-right";
    }

    if (collapseBtn && sidebar && mainContent) {
        collapseBtn.addEventListener("click", () => {
            sidebar.classList.toggle("collapsed");
            mainContent.classList.toggle("sidebar-collapsed");
            const isCollapsed = sidebar.classList.contains("collapsed");

            if (toggleIcon) {
                toggleIcon.className = isCollapsed
                    ? "fa-solid fa-chevron-right"
                    : "fa-solid fa-chevron-left";
            }

            localStorage.setItem("medshield_sidebar_collapsed", isCollapsed);
        });
    }

    // =====================================================================
    // 3. SIDEBAR — Mobile overlay toggle
    // =====================================================================
    const mobileSidebarBtn = document.getElementById("mobile-sidebar-toggle-btn");

    if (mobileSidebarBtn && sidebar) {
        mobileSidebarBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            sidebar.classList.toggle("show-mobile");
        });

        // Close when clicking outside
        document.addEventListener("click", (e) => {
            if (
                sidebar.classList.contains("show-mobile") &&
                !sidebar.contains(e.target) &&
                e.target !== mobileSidebarBtn
            ) {
                sidebar.classList.remove("show-mobile");
            }
        });
    }


    // =====================================================================
    // 4. LOGOUT
    //    Both the sidebar logout button and any page with class .logout-btn
    // =====================================================================
    function doLogout(e) {
        if (e) e.preventDefault();
        ["medshield_access_token",
         "medshield_refresh_token",
         "medshield_active_consultation_id",
         "medshield_active_consultation_patient_name",
         "medshield_active_consultation_patient_age",
         "medshield_active_consultation_patient_gender"
        ].forEach(k => localStorage.removeItem(k));
        window.location.href = "/login";
    }

    // Sidebar dedicated logout button
    const sidebarLogoutBtn = document.getElementById("sidebar-logout-btn");
    if (sidebarLogoutBtn) {
        sidebarLogoutBtn.addEventListener("click", doLogout);
    }

    // Any element with class .logout-btn or id="logout-btn" on any page
    document.querySelectorAll(".logout-btn, #logout-btn").forEach(btn => {
        btn.addEventListener("click", doLogout);
    });


    // =====================================================================
    // 5. DOCTOR PROFILE — Populate sidebar + navbar
    //    Fetches /api/auth/me and fills name, specialty, avatar initials
    // =====================================================================
    const path = window.location.pathname;
    const isPublicPage = ["/login", "/register"].includes(path);

    if (!isPublicPage) {
        fetch("/api/auth/me", {
            headers: {
                "Authorization": "Bearer " + (localStorage.getItem("medshield_access_token") || "")
            }
        })
        .then(res => {
            if (res.status === 401) {
                localStorage.removeItem("medshield_access_token");
                window.location.href = "/login";
                return null;
            }
            return res.json();
        })
        .then(data => {
            if (!data || !data.full_name) return;

            const initials = data.full_name
                .split(" ")
                .map(n => n[0])
                .join("")
                .toUpperCase()
                .substring(0, 2);

            const specialty = data.specialty || "Clinical Expert";

            // --- Sidebar Footer ---
            const sidebarName     = document.getElementById("sidebar-doc-name");
            const sidebarSpec     = document.getElementById("sidebar-doc-specialty");
            const sidebarAvatar   = document.getElementById("sidebar-doc-avatar");

            if (sidebarName)   sidebarName.textContent   = data.full_name;
            if (sidebarSpec)   sidebarSpec.textContent   = specialty;
            if (sidebarAvatar) sidebarAvatar.textContent = initials;

            // --- Navbar Doctor Button ---
            const navbarName   = document.getElementById("navbar-doc-name");
            const navbarAvatar = document.getElementById("navbar-doc-avatar");

            if (navbarName)   navbarName.textContent   = data.full_name;
            if (navbarAvatar) navbarAvatar.textContent = initials;
        })
        .catch(err => {
            console.warn("[MedShield-X] Doctor profile fetch failed:", err);
        });
    }


    // =====================================================================
    // 6. ACTIVE CONSULTATION CONTEXT
    //    Populate sidebar patient badge and other context elements
    // =====================================================================
    const consultationId  = localStorage.getItem("medshield_active_consultation_id");
    const patientName     = localStorage.getItem("medshield_active_consultation_patient_name");

    if (consultationId && patientName) {
        // Sidebar patient name badge (kept from old sidebar for page backwards compat)
        const sidebarPatientName = document.getElementById("sidebar-patient-name");
        if (sidebarPatientName) {
            sidebarPatientName.textContent = patientName;
        }

        // Active patient banner (used on some pages)
        const bannerEl = document.getElementById("active-patient-banner");
        if (bannerEl) bannerEl.classList.remove("d-none");

        const bannerNameEl = document.getElementById("sidebar-active-patient-name");
        if (bannerNameEl) bannerNameEl.textContent = patientName;
    }


    // =====================================================================
    // 7. GLOBAL AUTHENTICATED FETCH HELPER
    //    Usage: await medshieldFetch('/api/...', { method: 'POST', body: ... })
    // =====================================================================
    window.medshieldFetch = async function (url, options = {}) {
        const token = localStorage.getItem("medshield_access_token");
        if (!options.headers) options.headers = {};
        if (token) options.headers["Authorization"] = "Bearer " + token;

        const response = await fetch(url, options);

        if (response.status === 401) {
            localStorage.removeItem("medshield_access_token");
            localStorage.removeItem("medshield_refresh_token");
            window.location.href = "/login";
            return null;
        }
        return response;
    };


    // =====================================================================
    // 8. CHART.JS THEME HELPER
    //    Returns theme-appropriate colors for Chart.js
    //    Usage: const colors = MedShieldChartTheme.get()
    // =====================================================================
    window.MedShieldChartTheme = {
        get() {
            const isDark = document.documentElement.getAttribute("data-theme") === "dark";
            return {
                text:       isDark ? "#94A3B8" : "#64748B",
                grid:       isDark ? "rgba(255,255,255,0.05)" : "rgba(0,0,0,0.06)",
                tick:       isDark ? "#64748B" : "#94A3B8",
                background: isDark ? "#151B2C" : "#FFFFFF",
                primary:    "#2563EB",
                accent:     "#06B6D4",
                success:    "#10B981",
                warning:    "#F59E0B",
                danger:     "#EF4444",
            };
        },

        apply(chart) {
            const c = this.get();
            if (!chart || !chart.options) return;

            if (chart.options.plugins?.legend?.labels) {
                chart.options.plugins.legend.labels.color = c.text;
            }

            ["x", "y"].forEach(axis => {
                if (chart.options.scales?.[axis]) {
                    if (chart.options.scales[axis].grid) {
                        chart.options.scales[axis].grid.color = c.grid;
                    }
                    if (chart.options.scales[axis].ticks) {
                        chart.options.scales[axis].ticks.color = c.tick;
                    }
                }
            });

            chart.update();
        }
    };

    // Auto-update all registered charts when theme changes
    document.addEventListener("medshield:themechange", () => {
        if (window._medshieldCharts && Array.isArray(window._medshieldCharts)) {
            window._medshieldCharts.forEach(chart => {
                MedShieldChartTheme.apply(chart);
            });
        }
    });

    // Initialize global chart registry
    window._medshieldCharts = window._medshieldCharts || [];

});
