
const cookie = {
    // Create cookie
    add: function (name, value, days) {
        let expires;
        if (days) {
            let date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires='" + date.toUTCString();
        } else {
            expires = "";
        }
        document.cookie = name + "=" + value + expires + "'; path=/; samesite=lax";
    },
    // Read cookie
    get: function (name) {
        let nameEQ = name + "=";
        let ca = document.cookie.split(";");
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === " ") {
                c = c.substring(1, c.length);
            }
            if (c.indexOf(nameEQ) === 0) {
                return c.substring(nameEQ.length, c.length);
            }
        }
        return null;
    },
};

// Ghetto detect and set dark mode
if (cookie.get("theme") === null) {
    if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
        cookie.add("theme", "dark", 365); // default dark mode
        location.reload();
    } else {
        cookie.add("theme", "light", 365); // default light mode
    }
}
