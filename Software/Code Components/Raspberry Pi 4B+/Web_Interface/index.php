<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title> Assistant Credentials Management</title>
    <style>
.container {
    max-width: 600px;
    margin: 50px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.container {
  max-width: 400px;
  margin: 50px auto;
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.container label {
  font-weight: bold;
}

.container input[type="text"] {
  width: 100%;
  padding: 10px;
  margin: 8px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.container button {
  background-color: #990000;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
}

.container button:hover {
  background-color: #45a049;
}

h1 {
    text-align: center;
    margin-bottom: 20px;
}

form {
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 5px;
}

input[type="text"] {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }

        th, td {
            padding: 8px;
            border: 1px solid #ddd;
            text-align: left;
        }

        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }

        tr:nth-child(even) {
            background-color: #f2f2f2;
        }

        tr:hover {
            background-color: #ddd;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>User API Management</h1>
        <form id="apiForm" action="add_user.php" method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
            <label for="apiKey">API Key:</label>
            <input type="text" id="apiKey" name="apiKey" required>
            <button type="submit">Submit</button>
        </form>
        <?php
        // Aici facem rost de $output
        $output = shell_exec('./displaydb.sh 2>&1');
        
        if ($output !== null) {
            // Sparge output in un array the rows
            $rows = explode("\n", $output);
            // Output table header
            echo "<h2>Database Visualiser</h2>";
            echo "<table>";
            echo "<thead><tr><th>Username</th><th>API Key</th><th>Action</th></tr></thead>";
            echo "<tbody>";

            // Output table rows
foreach ($rows as $row) {
        // Skip empty rows
        if (empty($row)) {
            continue;
        }

        $columns = explode("|", $row);
        echo "<tr>";
        foreach ($columns as $column) {
            echo "<td>$column</td>";
        }
        echo "<td><button class='deleteBtn'>Delete</button></td>";
        echo "</tr>";
    }
            echo "</tbody>";
            echo "</table>";
        } else {
            echo "Error executing the script.";
        }
        ?>
<form id="apiKeyForm" action="apiloader.php" method="post">
  <label for="apiKey">Username or API Key Holder:</label><br>
  <input type="text" id="apiKey" name="apiKey"><br><br>
  <button type="submit">Load Key To Assistant</button>
</form>

    </div>
<script>
    document.querySelectorAll('.deleteBtn').forEach(button => {
        button.addEventListener('click', function() {
            var username = this.parentElement.previousElementSibling.previousElementSibling.textContent;
            var xhr = new XMLHttpRequest();
            xhr.open('POST', 'deleteuser.php', true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.onreadystatechange = function() {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    if (xhr.status === 200) {
                        alert(xhr.responseText);
                    } else {
                        alert('Error: ' + xhr.statusText);
                    }
                }
            };
            xhr.send('username=' + encodeURIComponent(username));
        });
    });
</script>

</body>
</html>
