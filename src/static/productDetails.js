document.addEventListener("DOMContentLoaded", () => {
    const productCards = document.querySelectorAll(".product-card");
    const detailModal = document.getElementById("product-detail-modal");
    const detailContent = document.getElementById("product-detail-content");
    const closeButton = document.createElement("button");
    closeButton.className = "modal-close";
    closeButton.innerHTML = "&times;";

    // Add loading spinner
    const loadingSpinner = document.createElement("div");
    loadingSpinner.className = "loading-spinner";
    loadingSpinner.style.display = "none";
    document.body.appendChild(loadingSpinner);

    productCards.forEach(card => {
        card.addEventListener("click", async () => {
            const productId = card.getAttribute("data-id");
            loadingSpinner.style.display = "block";

            try {
                const response = await fetch(`/api/product/${productId}`);
                if (!response.ok) {
                    throw new Error("Failed to fetch product details");
                }
                const product = await response.json();

                detailContent.innerHTML = `
                    <div class="product-detail">
                        <div class="product-image">
                            <img src="${product.image_url}" alt="${product.name}">
                        </div>
                        <div class="product-info">
                            <h1>${product.name}</h1>
                            <div class="info-row">
                                <span class="label">Age:</span>
                                <span class="value">${product.age} years</span>
                            </div>
                            <div class="description">
                                <p>${product.description}</p>
                            </div>
                            <div class="price-section">
                                <span class="price">$${product.price}</span>
                                <button class="adopt-button">Adopt Now</button>
                            </div>
                            <div id="seller-details" class="seller-details">
                                <!-- Seller details will be loaded here -->
                            </div>
                        </div>
                    </div>
                `;

                const adoptButton = detailContent.querySelector(".adopt-button");
                adoptButton.addEventListener("click", async () => {
                    const sellerDetailsDiv = document.getElementById("seller-details");
                    sellerDetailsDiv.innerHTML = "Loading seller details...";

                    try {
                        const sellerResponse = await fetch(`/api/seller/${product.seller_id}`);
                        if (!sellerResponse.ok) {
                            throw new Error("Failed to fetch seller details");
                        }
                        const seller = await sellerResponse.json();

                        sellerDetailsDiv.innerHTML = `
                            <div class="seller-info">
                                <h2>Seller Details</h2>
                                <p><strong>Name:</strong> ${seller.seller_name}</p>
                                <p><strong>Phone:</strong> ${seller.phone_number}</p>
                                <p><strong>Address:</strong> ${seller.address}</p>
                                <p><strong>Home Delivery:</strong> ${seller.home_delivery ? "Yes" : "No"}</p>
                            </div>
                        `;
                    } catch (error) {
                        console.error(error.message);
                        sellerDetailsDiv.textContent = "Unable to load seller details. Please try again.";
                    }
                });

                detailModal.appendChild(closeButton);
                detailModal.classList.add("fade-in");
                detailModal.style.display = "block";
            } catch (error) {
                console.error(error.message);
                showErrorMessage("Unable to load product details. Please try again later.");
            } finally {
                loadingSpinner.style.display = "none";
            }
        });
    });

    // Close modal on close button click
    closeButton.addEventListener("click", (e) => {
        e.stopPropagation();
        closeModal();
    });

    // Close modal on escape key
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            closeModal();
        }
    });

    // Close modal on outside click
    detailModal.addEventListener("click", (e) => {
        if (e.target === detailModal) {
            closeModal();
        }
    });

    function closeModal() {
        detailModal.classList.add("fade-out");
        setTimeout(() => {
            detailModal.style.display = "none";
            detailModal.classList.remove("fade-out");
        }, 300);
    }

    function showErrorMessage(message) {
        const errorDiv = document.createElement("div");
        errorDiv.className = "error-message";
        errorDiv.textContent = message;
        document.body.appendChild(errorDiv);

        setTimeout(() => {
            errorDiv.remove();
        }, 3000);
    }
});