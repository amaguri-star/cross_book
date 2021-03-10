$(document).on('click', '.upload-portfolio-image-btn', function () {
    var inputToUploadPortfolioImage = $(this).next('.upload-portfolio-image')
    var portfolioImageGroup = inputToUploadPortfolioImage.closest('.form-row').next().next('.portfolio-image-group')

    inputToUploadPortfolioImage.click()
    inputToUploadPortfolioImage.off('change').on('change', function (e) {
        if (e.target.files && e.target.files[0]) {
            var files = e.target.files
            for (var i = 0; i < files.length; i++) {
                var file = files[i]
                var reader = new FileReader()
                reader.onload = function (e) {
                    portfolioImageGroup.append(`
              <div class="form-group col-md-3">
                <div class="responsive-img-wrapper portfolio-image">
                  <div class="responsive-img" style="background-image: url(${e.target.result})">
                  </div>
                </div>
              </div>`)
                }
                reader.readAsDataURL(file)
            }
        }
    })
})