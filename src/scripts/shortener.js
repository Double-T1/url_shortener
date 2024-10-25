import Alpine from "alpinejs";


Alpine.data("shortener", () => ({
    shortCode: "",
    isChecked: false,
    showMessage: true,

    init() {
        this.getShortCode();
        this.$refs.remarkArea.value = "";

        this.$refs.shortCodeInput.addEventListener("htmx:afterSettle", () => {
           this.getShortCode();
        })

        this.$refs.message.addEventListener("htmx:afterSettle", () => {
           this.showMessage = true;
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
}));