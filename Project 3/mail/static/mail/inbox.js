
// new formatatted 
document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  function compose_email() {
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#open-email-view').style.display = 'none';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }

  function open_email(id) {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#open-email-view').style.display = 'block';

    console.log(id);

    fetch(`/emails/${id}`)
      .then(response => response.json())
      .then(email => {
        // Print email
        console.log(email);

        //for the selected email add the following in the open-mail-view
        document.querySelector('#open-email-view').innerHTML = `
          <div class="container">
            <h5><strong>From: </strong>${email.sender}</h5>
            <h5><strong>To: </strong>${email.recipients}</h5>
            <h5><strong>Subject: </strong>${email.subject}</h5>
            <h5><strong>Timestamp: </strong>${email.timestamp}</h5>
          </div>
          <div class="container my-3">
            <ul class="list-group">
              <li class="list-group-item">${email.body}</li>
            </ul>
          </div>`;


        // archive functionality   
        const archive_btn = document.createElement('button'); //creating a button element 
        archive_btn.className = email.archived ? 'btn btn-outline-danger' : 'btn btn-outline-success'; //css for button depending on archive status
        archive_btn.innerHTML = email.archived ? 'Unarchive' : 'Archive'; //text for button
        
        //call to api to change archive status when clicked
        archive_btn.addEventListener('click', () => {
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: !email.archived //toggling the status for the archive
            })
          })

            // loading the archive page when clicked
            .then(() => {
              load_mailbox('inbox');
            });
        });

        // email read/unread
        if (!email.read) {
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
              read: true
            })
          });
        }
        document.querySelector('#open-email-view').append(archive_btn);// adding the button element to the open-mail-view html

        // reply functionality
        
        const reply_btn = document.createElement('button'); //creating the reply button element
        reply_btn.className = 'btn btn-outline-info'; //css styling for reply button
        reply_btn.innerHTML = 'Reply'; //giving the value of the btn
        
        reply_btn.addEventListener('click', () => { 
          compose_email();
          
          let subject = email.subject;
          //check if the subject starts with Re:
          if (!subject.startsWith('Re:')) {
            subject = 'Re:' + subject;
        }

          document.querySelector('#compose-recipients').value = email.sender;
          document.querySelector('#compose-subject').value = subject;
          document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.subject}`
          
        });
        
        document.querySelector('#open-email-view').append(reply_btn);// addiing the reply btn element to html page
      });
  }

  function load_mailbox(mailbox) {
    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#open-email-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    //getting the mailbox
    fetch(`/emails/${mailbox}`)
      .then(response => response.json())
      .then(emails => {
        // Print emails
        console.log(emails);
        // loop for each email
        emails.forEach(mail => {

          const emailItem = document.createElement('div');
          emailItem.className = 'list-group-item';

          // defining what is shown in each div 
          emailItem.innerHTML = `
            <h5>${mail.subject}</h5>
            <h6>${mail.recipients}</h6>
            <p>${mail.timestamp}</p>
          `;

          // Set background color based on the 'read' property
          if (mail.read) {
            emailItem.style.backgroundColor = 'gray';
          } else {
            emailItem.style.backgroundColor = 'white';
          }

          //event listener for when clicked on 
          emailItem.addEventListener('click', () => open_email(mail.id));
          document.querySelector('#emails-view').append(emailItem);
        });
      });
  }


  document.querySelector('#compose-form').addEventListener('submit', send_email);
  
  function send_email(event) {
   
    event.preventDefault();
    //getting the data entered from the forms
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    // sending the data to the backend
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
      }),
    })
      .then(response => response.json())
      .then(result => {
        console.log(result); // Print the response
        load_mailbox('sent');
      })
      .catch(error => console.error('Error sending email:', error));
  }

});
