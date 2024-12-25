PWeb.RPIR = (function () {

    function showHideBankingInfo(isShow = true) {
        let banking = jQuery(".banking")
        let bankingInput = jQuery(".banking-input")
        if (isShow) {
            banking.show()
            bankingInput.attr("required", true)
        } else {
            banking.hide()
            bankingInput.removeAttr("required")
        }
    }

    function showHideMobileBankingInfo(isShow = true) {
        let banking = jQuery(".mobile-banking")
        let bankingInput = jQuery(".mobile-banking-input")
        if (isShow) {
            banking.show()
            bankingInput.attr("required", true)
        } else {
            banking.hide()
            bankingInput.removeAttr("required")
        }
    }

    return {
        printDocument: function () {
            jQuery(".print-info").click(function () {
                let printableArea = jQuery(".printable-data").html();
                let newWindow = window.open();
                let newDocument = newWindow.document;
                newDocument.write(printableArea);
                newDocument.close();
                newWindow.print();
                return false
            })
        },
        showHideBankingInformation: function () {
            showHideBankingInfo(false)
            jQuery(".change-banking-type").change(function () {
                let _this = jQuery(this)
                let value = _this.val()
                if (value === "মোবাইল ব্যাংকিং") {
                    showHideMobileBankingInfo(true)
                    showHideBankingInfo(false)
                } else {
                    showHideMobileBankingInfo(false)
                    showHideBankingInfo(true)
                }
            })
        },
        copyAddress: function () {
            jQuery("#same-as-permanent-address").change(function () {
                    let data = ["division", "union", "district", "post", "upozila", "village"]
                    for (let index in data) {
                        let item = data[index]
                        let source = jQuery(".from-" + item)
                        let destination = jQuery(".to-" + item)
                        if (source.val() !== "" && destination.val() === "") {
                            destination.val(source.val())
                        }
                    }
                }
            )
        },
        init: function () {
            PWeb.RPIR.copyAddress()
            PWeb.RPIR.printDocument()
            PWeb.RPIR.showHideBankingInformation()
        }
    }


}());

jQuery(document).ready(function () {
    PWeb.RPIR.init();
});