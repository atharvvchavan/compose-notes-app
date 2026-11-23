// Letter counter
const box = document.getElementById("text");
const counter = document.getElementById("counter");

box.addEventListener("input", () => {
    counter.textContent = box.value.length + " / 500";
});

// Ctrl+Enter sends the note
box.addEventListener("keydown", (event) => {
    if (event.ctrlKey && event.key === "Enter") {
        box.form.requestSubmit();
    }
});

// Ask before deleting
document.querySelectorAll(".del-form").forEach((form) => {
    form.addEventListener("submit", (event) => {
        if (!confirm("Delete this note?")) {
            event.preventDefault();
        }
    });
});