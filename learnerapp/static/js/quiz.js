const options = document.querySelectorAll('.option');
const submit_button = document.querySelector('#submit');

options.forEach(option => {
    let option_value = option.innerText;
    if (option_value.charAt(0) === '-') {
        option.innerText = option_value.substring(1);
        option.classList.add('correct');
    }
    option.addEventListener('click', () => {
        option.classList.toggle('selected');
        let parentElement = option.parentElement

        let children = parentElement.children;

        for (let i = 0; i < children.length; i++) {
            children[i].disabled = true;
        }
    });
});

submit_button.addEventListener('click', () => {
    let score = 0
    let selected_options = document.querySelectorAll('.selected');
    selected_options.forEach(option => {
        if (option.classList.contains('correct')) {
            score++
        }
    })

    fetch(`/submit_quiz/${score}`)
    .then((response) => response.json())
        .then((message)=> {
            alert(message['message'])
            window.location.href = '/';
        })

});