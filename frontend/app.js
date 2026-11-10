document.getElementById('tracker-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Αποτρέπει την ανανέωση της σελίδας όταν πατάς "Enter"

    // Παίρνουμε τις τιμές που πληκτρολόγησες στα πεδία της φόρμας
    const url = document.getElementById('url').value;
    const price = parseFloat(document.getElementById('price').value);
    const email = document.getElementById('email').value;

    // Ετοιμάζουμε τα δεδομένα στη μορφή που τα περιμένει το Pydantic μοντέλο σου (JSON)
    const productData = {
        product_url: url,
        target_price: price,
        user_email: email
    };

    const messageBox = document.getElementById('message-box');

    try {
        // Στέλνουμε το POST request στο FastAPI (προϋποθέτει ότι ο server τρέχει στο port 8000)
        const response = await fetch('http://127.0.0.1:8000/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(productData)
        });

        if (response.ok) {
            messageBox.textContent = "Επιτυχία! Το προϊόν καταχωρήθηκε στη βάση.";
            messageBox.style.color = "green";
            document.getElementById('tracker-form').reset(); // Αδειάζει τη φόρμα για το επόμενο προϊόν
        } else {
            messageBox.textContent = "Υπήρξε πρόβλημα κατά την προσθήκη.";
            messageBox.style.color = "red";
        }
    } catch (error) {
        console.error("Σφάλμα:", error);
        messageBox.textContent = "Αδυναμία σύνδεσης. Βεβαιώσου ότι το FastAPI τρέχει στο terminal.";
        messageBox.style.color = "red";
    }

    messageBox.classList.remove('hidden');
});