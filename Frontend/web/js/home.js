document.addEventListener('DOMContentLoaded', function() {
    // Existing logic for logout and modal triggers
    document.querySelectorAll('button').forEach(button => {
        if (button.textContent.includes('LOGOUT')) {
            button.addEventListener('click', function() {
                console.log('Logout button clicked');
                window.location.href = 'login.html';
            });
        } else if (button.textContent.includes('CREATE CHAT')) {
            button.setAttribute('data-toggle', 'modal');
            button.setAttribute('data-target', '#createGroupModal');
        } else if (button.textContent.includes('JOIN CHAT')) {
            button.setAttribute('data-toggle', 'modal');
            button.setAttribute('data-target', '#joinGroupModal');
        }
    });

    const modalCreateChatButton = document.querySelector('#createGroupModal .btn-primary');
    const modalJoinChatButton = document.querySelector('#joinGroupModal .btn-primary');

    const chatNameInput = document.getElementById('new-group-name');
    const chatIdInput = document.getElementById('group-id');

    const promptJoinCreateChat = document.getElementById('promptJoinCreateChat');
    const messageForm = document.getElementById('messageAndPlaneIcon');

    const chatNameText = document.getElementById('chatNameText');

    function toggleChatUI(hasJoined) {
        if (hasJoined) {
            promptJoinCreateChat.style.display = 'none'; // Hide the prompt
            // the content of the messageForm should be this:
            // <input class="form-control" type="text" placeholder="Escribe aqui el mensaje que quieras enviar" style="width: 80%;">
            // <button class="btn btn-outline-success" type="button"><i class="fas fa-paper-plane"></i></button>
            messageForm.innerHTML = `
                <input class="form-control" type="text" placeholder="Escribe aqui el mensaje que quieras enviar" style="width: 80%;">
                <button class="btn btn-outline-success" type="button"><i class="fas fa-paper-plane"></i></button>
            `;

            const sendMessageButton = messageForm.querySelector('.btn-outline-success');
            const messageInput = messageForm.querySelector('.form-control');

            sendMessageButton.addEventListener('click', function() {
                const message = messageInput.value;
                const chat_id = getCookie('chat_id'); // Assuming you're setting this cookie somewhere
                const user_id = getCookie('user_id');

                if(message && chat_id && user_id) {
                    eel.send_tcp_message_eel(chat_id, user_id, message);
                    messageInput.value = ''; // Clear the input after sending the message
                } else {
                    alert('Message, chat ID, or user ID is missing.');
                }
            });
        
            

        } else {
            promptJoinCreateChat.style.display = 'block'; // Show the prompt
            // the content of the messageForm should be null
            messageForm.innerHTML = '';
            
        }
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Initially call toggleChatUI with false to show the prompt and hide the form
    toggleChatUI(false);

    // Create chat event listener
    modalCreateChatButton.addEventListener('click', function() {
        const chatName = chatNameInput.value;
        fetch('http://127.0.0.1:6789/create_chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ chat_name: chatName }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Chat created successfully. Chat ID: ' + data.chat_id);
                document.cookie = `chat_id=${data.chat_id}`;
                $('#createGroupModal').modal('hide');
                toggleChatUI(true); // User has joined a chat, so toggle UI accordingly
                chatNameText.innerHTML = chatName;
            } else {
                alert('Failed to create chat');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error creating chat');
        });
    });

    // Join chat event listener
    modalJoinChatButton.addEventListener('click', function() {
        const chatId = chatIdInput.value;
        fetch('http://127.0.0.1:6789/get_chat_information', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ chat_id: chatId }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Chat joined successfully. Chat Name: ' + data.chat_info[1] + ' Chat ID: ' + data.chat_info[0]);
                document.cookie = `chat_id=${data.chat_info[0]}`;
                $('#joinGroupModal').modal('hide');
                toggleChatUI(true); // User has joined a chat, so toggle UI accordingly
                chatNameText.innerHTML = data.chat_info[1];
            } else {
                alert('Failed to join chat');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert(error.message);
        });
    });
});
