

// this entire file is Not in use yet


// search
        document.getElementById("searchDropdown").addEventListener("click", function (event) {
            var searchDropdownContent = document.querySelector(".search-dropdown-content");
            searchDropdownContent.style.display = (searchDropdownContent.style.display === "block") ? "none" : "block";
            event.stopPropagation();
        });
    
        document.querySelector(".search-dropdown-content input[type='text']").addEventListener("click", function (event) {
            event.stopPropagation();
        });
    
        document.addEventListener("click", function (event) {
            var searchDropdownContent = document.querySelector(".search-dropdown-content");
            if (event.target.closest(".search-dropdown") === null) {
                searchDropdownContent.style.display = "none";
            }
        });

// top right menu
        document.getElementById("dropdownBtn").addEventListener("click", function (event) {
                var dropdownContent = document.querySelector(".dropdown-content");
                dropdownContent.style.display = (dropdownContent.style.display === "block") ? "none" : "block";
                event.stopPropagation();
            });

            document.addEventListener("click", function (event) {
                var dropdownContent = document.querySelector(".dropdown-content");
                if (event.target.closest(".dropdown") === null) {
                    dropdownContent.style.display = "none";
                }
            });




// copy to Clipboard - not being used yet
            document.addEventListener("DOMContentLoaded", function () {
                const copyLinkBtn = document.getElementById("copy-link-btn");
            
                copyLinkBtn.addEventListener("click", function () {
                    // logic to copy the link to the clipboard -a library like Clipboard.js can be used
                    // Example using Clipboard.js: https://clipboardjs.com/
                    // '#my-link-id' to be replaced with the actual ID of the link you want to copy
                    const linkToCopy = document.querySelector("#my-link-id");
                    new ClipboardJS(copyLinkBtn, {
                        text: function () {
                            return linkToCopy.href;
                        }
                    });
            
                    // You may want to provide feedback to the user (e.g., show a tooltip)
                    alert("Link copied to clipboard!");
                });
            });