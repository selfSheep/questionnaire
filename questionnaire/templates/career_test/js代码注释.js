        function test_finished() {
            var class_anwsers = document.getElementsByClassName("btn-info");
            var question_and_anwser_array = new Array();
            for (var i = 0;  i < class_anwsers.length; i++) {
                question_and_anwser_array.push(class_anwsers[i].getAttribute("data-anwser"));
            }
            var datas = JSON.stringify(question_and_anwser_array);
            console.log(datas);
                $.ajax({
                    type: "POST",
                    dataType: "json",
                    url: "{% url 'handle_anwser' %}",
                    data: {'datas': datas, 'test_type': '{{ test_type }}', 'csrfmiddlewaretoken': '{{ csrf_token }}'},
                    success: function (data) {
                      alert('成功');
                    },
                    error: function () {
                        alert('错误');
                    }
                });
        }