document.addEventListener('DOMContentLoaded', function() {
    // Existing logic for logout and modal triggers
    document.querySelectorAll('button').forEach(button => {
        if (button.textContent.includes('LOGOUT')) {
            button.addEventListener('click', function() {
                console.log('Logout button clicked');
                window.location.href = 'login.html';
            });
        } else if (button.textContent.includes('CREATE CHAT')) {
            // Corrected to match the button text. Ensure this matches your actual button text.
            button.setAttribute('data-toggle', 'modal');
            button.setAttribute('data-target', '#createGroupModal');
        } else if (button.textContent.includes('JOIN CHAT')) {
            // Corrected to match the button text. Ensure this matches your actual button text.
            button.setAttribute('data-toggle', 'modal');
            button.setAttribute('data-target', '#joinGroupModal');
        }
    });

    // Additional logic for API calls
    const modalCreateChatButton = document.querySelector('#createGroupModal .btn-primary');
    const modalJoinChatButton = document.querySelector('#joinGroupModal .btn-primary');

    const chatNameInput = document.getElementById('new-group-name');
    const chatIdInput = document.getElementById('group-id');

    const promptJoinCreateChat = document.getElementById('promptJoinCreateChat');
    const messageForm = document.getElementById('messageForm');

    function initializeChatUI() {
        promptJoinCreateChat.style.display = 'block'; // Show the prompt
        messageForm.style.display = 'none'; // Hide the form
    }

    initializeChatUI();



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
                $('#createGroupModal').modal('hide');
                promptJoinCreateChat.style.display = 'none';
                messageForm.style.display = 'flex'; // Use 'flex' to keep the form's styling
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
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Chat not found');
            }
        })
        .then(data => {
            if (data.success) {
                alert('Chat joined successfully. Chat Info: ' + JSON.stringify(data.chat_info));
                $('#joinGroupModal').modal('hide');
                promptJoinCreateChat.style.display = 'none';
                messageForm.style.display = 'flex'; // Use 'flex' to keep the form's styling
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
