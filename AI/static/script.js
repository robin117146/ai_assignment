
	<script>
function showDetails(name, details) {
    const modal = document.getElementById("elementModal");
    document.getElementById("elementName").textContent = name;
    document.getElementById("elementDetails").textContent = details;
    modal.style.display = "flex";
}

function closeModal() {
    const modal = document.getElementById("elementModal");
    modal.style.display = "none";
}

// Close modal when clicking outside the modal content
window.onclick = function(event) {
    const modal = document.getElementById("elementModal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
};
</script>