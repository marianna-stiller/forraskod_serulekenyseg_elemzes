// in action_page.php
<?php
// connecting to db by the name of sql_injection
$con = new PDO('mysql:host=localhost;dbname=sql_injection', 'root', '');
// OR
$con = new mysqli("localhost", "root", "", "sql_injection");

// processing form input
if (isset($_POST['email']))
{
    $email = $_POST['email'];
    $query = $con->query("SELECT * FROM users WHERE email = '{$email}'");
    // for PDO
    if ($query->rowCount())
    {
        echo "found an email address!";
    }

    // for MYSQL
    if ($query->num_rows)
    {
        echo "found an email address!";
    }
}

// ... hidden body of the form