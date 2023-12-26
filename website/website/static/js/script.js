function subscribe_call() {
    let text = document.getElementById("floatingInput").value;
    let data = new FormData();
    data.append('text', text);
    let validator = /\S+@\S+\.\S+/;
    if (validator.test(text)) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: "/save/",
            data: data,
            processData: false,
            contentType: false,
            success: function (response) {
                // Обработка успешного ответа от сервера
                console.log(response);
                // Hide elements on successful response
                document.getElementById("button-inp").style.display = "none";
                document.getElementById("mail-inp").style.display = "none";
                document.getElementById("thx-id").style.display = "block";
            },
            error: function (error) {
                // Обработка ошибки
                console.log(error);
            }
        });
    }
}
function scrollToHeight(height) {
      window.scrollTo({
        top: height,
        behavior: 'smooth' //Добавляет плавность прокрутке
      });
}
function get_result() {
    // получение данных
    let data = new FormData();
    let name = document.getElementById('my-name').value;
    data.append('name', name);
    let good_program = document.getElementById('my-good-program-select').value;
    data.append('my_good_program', good_program);
    let favorite1 = document.getElementById('flexCheckDefault1');
    if (favorite1.checked) {
        data.append('favorite1', '1');
    } else {
        data.append('favorite1', '0');
    }
    let favorite2 = document.getElementById('flexCheckDefault2');
    if (favorite2.checked) {
        data.append('favorite2', '1');
    } else {
        data.append('favorite2', '0');
    }
    let favorite3 = document.getElementById('flexCheckDefault3');
    if (favorite3.checked) {
        data.append('favorite3', '1');
    } else {
        data.append('favorite3', '0');
    }
    let favorite4 = document.getElementById('flexCheckDefault4');
    if (favorite4.checked) {
        data.append('favorite4', '1');
    } else {
        data.append('favorite4', '0');
    }
    let favorite5 = document.getElementById('flexCheckDefault5');
    if (favorite5.checked) {
        data.append('favorite5', '1');
    } else {
        data.append('favorite5', '0');
    }
    let favorite_png1 = document.getElementById('flexRadioDefault1');
    let favorite_png2 = document.getElementById('flexRadioDefault2');
    let favorite_png3 = document.getElementById('flexRadioDefault3');
    if (favorite_png1.checked) {
        data.append('favorite_png', '1');
    } else if (favorite_png2.checked) {
        data.append('favorite_png', '2');
    } else {
        data.append('favorite_png', '3');
    }
    if (name == '') {
        document.getElementById('my-name').placeholder = 'Пожалуйста, введите имя!';
        scrollToHeight(0);
        if (!favorite_png1.checked && !favorite_png2.checked && !favorite_png3.checked) {
            document.querySelector('#my-h-id').innerHTML = 'Пожалуйста, выберите хотя бы одну картинку!';
        }
    } else if (!favorite_png1.checked && !favorite_png2.checked && !favorite_png3.checked) {
        document.querySelector('#my-h-id').innerHTML = 'Пожалуйста, выберите хотя бы одну картинку!';
        scrollToHeight(1900);
    } else {
        $.ajax({
            type: "POST",
            url: "/save_quiz/",
            data: data,
            processData: false,
            contentType: false,
            success: function (response) {
                // Обработка успешного ответа от сервера
                console.log(response);
                // Скрытие элементов
                document.getElementById("my-container-1").style.display = "none";
                document.getElementById("my-container-2").style.display = "none";
                document.getElementById("my-container-3").style.display = "none";
                document.getElementById("my-container-4").style.display = "none";
                document.getElementById("my-container-5").style.display = "none";
                document.getElementById("my-container-6").style.display = "block";
                document.getElementById("my-container-7").style.display = "block";
                document.getElementById("my-container-8").style.display = "block";

                $.ajax({
                    url: '/statistic/',
                    type: 'GET',
                    success: function (response) {
                        document.getElementById('my-prog1').value = 'Положительно:' + response['program'][0].toString() + '%';
                        document.getElementById('my-prog2').value = 'Отрицательно:' + response['program'][1].toString() + '%';

                        document.getElementById('my-lang1').value = 'С выбрали:' + response['language'][0].toString() + '%';
                        document.getElementById('my-lang2').value = 'С++ выбрали:' + response['language'][1].toString() + '%';
                        document.getElementById('my-lang3').value = 'С# выбрали:' + response['language'][2].toString() + '%';
                        document.getElementById('my-lang4').value = '1С выбрали:' + response['language'][3].toString() + '%';
                        document.getElementById('my-lang5').value = '++С выбрали:' + response['language'][4].toString() + '%';

                        document.getElementById('my-img1').value = '1 картинку выбрали:' + response['favorite'][0].toString() + '%';
                        document.getElementById('my-img2').value = '2 картинку выбрали:' + response['favorite'][1].toString() + '%';
                        document.getElementById('my-img3').value = '3 картинку выбрали:' + response['favorite'][2].toString() + '%';

                        console.log(response);
                    }
                });
            },
            error: function (error) {
                // Обработка ошибки
                console.log(error);
            }
        });
    }
}
