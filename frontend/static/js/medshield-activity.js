/**
 * MedShield-X Shared Activity Store
 * ------------------------------------
 * Provides a lightweight localStorage-based activity log that all analysis
 * pages write to and the dashboard reads from.
 *
 * Entry shape:
 * {
 *   type: 'medical_qa' | 'xray' | 'document' | 'report' | 'explainability',
 *   timestamp: ISO string,
 *   ... type-specific fields
 * }
 */

const MedShieldActivity = (() => {
    const STORE_KEY = 'medshield_activity_log';
    const MAX_ENTRIES = 100;

    function _load() {
        try {
            return JSON.parse(localStorage.getItem(STORE_KEY) || '[]');
        } catch {
            return [];
        }
    }

    function _save(entries) {
        try {
            localStorage.setItem(STORE_KEY, JSON.stringify(entries));
        } catch (e) {
            console.warn('[MedShieldActivity] localStorage write failed:', e);
        }
    }

    /**
     * Log a new activity entry.
     * @param {string} type - 'medical_qa' | 'xray' | 'document' | 'report' | 'explainability'
     * @param {object} data - Type-specific payload fields
     */
    function log(type, data) {
        const entries = _load();
        const entry = {
            type,
            timestamp: new Date().toISOString(),
            ...data
        };
        entries.unshift(entry); // newest first
        if (entries.length > MAX_ENTRIES) entries.length = MAX_ENTRIES;
        _save(entries);
    }

    /**
     * Return all logged entries, newest first.
     */
    function getAll() {
        return _load();
    }

    /**
     * Return the most recent entry of a given type, or null.
     * @param {string} type
     */
    function getLatest(type) {
        return _load().find(e => e.type === type) || null;
    }

    /**
     * Return all entries of a given type.
     * @param {string} type
     */
    function getByType(type) {
        return _load().filter(e => e.type === type);
    }

    /**
     * Return counts per type: { medical_qa: N, xray: N, document: N, report: N, explainability: N }
     */
    function getCounts() {
        const entries = _load();
        const counts = { medical_qa: 0, xray: 0, document: 0, report: 0, explainability: 0 };
        entries.forEach(e => {
            if (counts[e.type] !== undefined) counts[e.type]++;
        });
        counts.total = entries.length;
        return counts;
    }

    /**
     * Clear all activity logs.
     */
    function clear() {
        _save([]);
    }

    /**
     * Format a timestamp ISO string to a human-readable label.
     * @param {string} isoStr
     */
    function formatTime(isoStr) {
        if (!isoStr) return 'N/A';
        try {
            const d = new Date(isoStr);
            return d.toLocaleString('en-US', {
                month: 'short', day: 'numeric', year: 'numeric',
                hour: '2-digit', minute: '2-digit'
            });
        } catch {
            return isoStr;
        }
    }

    return { log, getAll, getLatest, getByType, getCounts, clear, formatTime };
})();

// Expose globally
window.MedShieldActivity = MedShieldActivity;
