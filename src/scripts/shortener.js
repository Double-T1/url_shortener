import Alpine from "alpinejs";


Alpine.data("shortener", () => ({
    shortCode: "",
    isChecked: false,
    showMessage: false,

    init() {
        this.getShortCode();

        this.$refs.shortCodeInput.addEventListener("htmx:afterSettle", () => {
           this.getShortCode();
        })

        this.$refs.message.addEventListener("htmx:afterSettle", () => {
           this.showMessage = true;
        })
    },

    getShortCode () {
        const labelShortCode = this.$refs.labelShortCode;
        this.shortCode = labelShortCode.dataset.code;
    },

    clearCheckBox() {
        this.isChecked = false;
        this.showMessage = false;
    }
}));