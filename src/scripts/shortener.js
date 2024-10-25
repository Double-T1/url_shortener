import Alpine from "alpinejs";


Alpine.data("shortener", () => ({
    shortCode: "",
    isChecked: false,
    showMessage: true,
    copyTooltip: "複製短網址",
    host: "",

    init() {
        this.getShortCode();
        this.$refs.remarkArea.value = "";
        this.host = this.$refs.labelShortCode.firstElementChild.textContent;

        this.$refs.shortCodeInput.addEventListener("htmx:afterSettle", () => {
           this.getShortCode();
        })

        this.$refs.message.addEventListener("htmx:afterSettle", () => {
            this.showMessage = true;
            if (this.$refs.message.firstElementChild.dataset.status === "copyShortUrl") {
                this.copyShortUrl();
            }
        })

        this.$refs.remarkBtn.addEventListener("htmx:beforeRequest", () => {
            this.$refs.remarkArea.value = "載入中請稍候...";
        })
    },

    getShortCode () {
        const labelShortCode = this.$refs.labelShortCode;
        this.shortCode = labelShortCode.dataset.code;
    },

    clearCheckBox() {
        this.isChecked = false;
        this.showMessage = false;
    },

    copyShortUrl() {
        navigator.clipboard.writeText(this.host + this.shortCode);
    }
}));