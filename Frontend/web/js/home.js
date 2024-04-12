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
                const chat_id = localStorage.getItem('chat_id');
                const user_id = localStorage.getItem('user_id');


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


    

    eel.expose(add_chat_message);
    function add_chat_message(user_id, username, message) {
        const chatMessages = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');

        // Username display
        const usernameDiv = document.createElement('div');
        usernameDiv.classList.add('username');
        usernameDiv.innerText = username;
        messageDiv.appendChild(usernameDiv);

        // Ensure user_id from the message and localStorage are compared correctly
        const localUserId = localStorage.getItem('user_id');
        // Parse user_id from the message to the same type as stored in localStorage, assuming localStorage stores IDs as strings
        user_id = user_id.toString();

        console.log(user_id, localUserId, message, username);

        if(user_id === localUserId) {
            messageDiv.classList.add('my-message');
        } else {
            messageDiv.classList.add('other-message');
        }

        const messageContentDiv = document.createElement('div');
        messageContentDiv.innerText = message;
        messageDiv.appendChild(messageContentDiv);

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to the bottom
    }


    





    // Initially call toggleChatUI with false to show the prompt and hide the form
    toggleChatUI(false);

    // Create chat event listener
    modalCreateChatButton.addEventListener('click', async function() {

        const chatName = chatNameInput.value;
        fetch('http://127.0.0.1:6789/api/create_chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ chat_name: chatName }),
        })
        .then(response => response.json())
        .then(async data => {
            if (data.success) {
                
                await eel.change_multicast_listening_port_eel(data.chat_id);
                
                
                alert('Chat created successfully. Chat ID: ' + data.chat_id);
                localStorage.setItem('chat_id', data.chat_id);
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
   // Join chat event listener
    // Join chat event listener
    modalJoinChatButton.addEventListener('click', function() {
        const chatId = chatIdInput.value;
        fetch('http://127.0.0.1:6789/api/get_chat_information', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ chat_id: chatId }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // First, change multicast listening port
                eel.change_multicast_listening_port_eel(data.chat_info[0]);
                
                // Fetch the chat history
                fetch('http://127.0.0.1:6789/api/get_chat_history', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ chat_id: chatId }),
                })
                .then(response => response.json())
                .then(historyData => {
                    if (historyData.success) {
                        // Loop through the chat history and add each message with the username
                        historyData.chat_history.forEach(message => {

                            add_chat_message(message.user_id, message.username, message.content);
                        });
                    } else {
                        alert('Failed to retrieve chat history.');
                    }
                })
                .catch(error => {
                    console.error('Error fetching chat history:', error);
                    alert('Error fetching chat history');
                });

                alert('Chat joined successfully. Chat Name: ' + data.chat_info[1] + ' Chat ID: ' + data.chat_info[0]);
                localStorage.setItem('chat_id', data.chat_info[0]);
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
