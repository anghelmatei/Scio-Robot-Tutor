<?php
// Preia username din Post req
$username = $_POST['apiKey'];

// Debugging: afiseaza username 
echo "Username received: $username\n";

// =Preia output si cauta cheia
$output = shell_exec('./displaydb.sh 2>&1');

if ($output !== null) {
    //Desparte intr-un array de randuri
    $rows = explode("\n", $output);

    //itereaza prin firecare row pentru a gasi username coresp si apikey
    foreach ($rows as $row) {
        // sari peste empty rows
        if (empty($row)) {
            continue;
        }
        //-||- arr de randuri
        $columns = explode("|", $row);

        //verifica daca prima coloanase potriveste
        if (trim($columns[0]) === $username) {
            //daca usernam se potriveste ia apikey
            $apiKey = trim($columns[1]);
            echo "ApiKey Found: $apiKey\n";

            // Paseaza catre scriptul care schimba apikey
            $envKeyModCommand = "bash envkeymod.sh " . $apiKey;
            $output = shell_exec($envKeyModCommand);

            echo "envkeymod.sh output: $output\n";

            //verifica daca comanda e succesfull
            if ($output === null) {
                echo "Error: Failed to set API key.";
            } else {
                echo "API key loaded successfully.";
            }

            break;
        }
    }
//daca loop se incheie fara a fi gasit username coresp, declanseaza o eroare
    if (!isset($apiKey)) {
        echo "No API key found for the provided username.";
    }
} else {
    echo "Error: Unable to retrieve data from the database.";
}
?>
