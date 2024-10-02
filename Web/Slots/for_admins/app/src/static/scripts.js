document.getElementById('spin-button').addEventListener('click', async function() {
    const reel1 = Math.floor(Math.random() * 10);
    const reel2 = Math.floor(Math.random() * 10);
    const reel3 = Math.floor(Math.random() * 10);

    document.getElementById('reel1').textContent = reel1;
    document.getElementById('reel2').textContent = reel2;
    document.getElementById('reel3').textContent = reel3;

    const hash = generateHash(reel1, reel2, reel3);

    fetch('/spin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            number1: reel1,
            number2: reel2,
            number3: reel3,
            hash: hash
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.new_balance !== undefined) {
            document.getElementById('balance').textContent = data.new_balance;
        }

        if (data.message) {
            document.getElementById('result').textContent = data.message;
        } else if (data.error) {
            document.getElementById('result').textContent = data.error;
        }
    })
    .catch(err => {
        console.error("Fetch error:", err);
        document.getElementById('result').textContent = "Error occurred. Try again.";
    });
});

function generateHash(num1, num2, num3) {
    const combined = `${num1}${num2}${num3}`;

    // Generate the SHA1 hash using crypto-js
    const sha1Hash = CryptoJS.SHA1(combined).toString();

    // Double MD5 the SHA1 hash
    const firstMd5 = CryptoJS.MD5(sha1Hash).toString();
    const finalMd5 = CryptoJS.MD5(firstMd5).toString();

    return finalMd5;
}
