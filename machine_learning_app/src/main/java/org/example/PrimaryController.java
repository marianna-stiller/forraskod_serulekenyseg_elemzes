package org.example;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.util.ResourceBundle;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Label;

public class PrimaryController implements Initializable {
    @FXML
    public Label result;

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        try {
            Runtime runtime = Runtime.getRuntime();
            runtime.exec("node parser.js");
            runtime.exec("py nodes.py");
            runtime.exec("py vectorizer.py");
            Process process = runtime.exec("py tanulo.py");
            InputStream is = process.getInputStream();
            InputStreamReader isr = new InputStreamReader(is);
            BufferedReader br = new BufferedReader(isr);
            String line;

            while ((line = br.readLine()) != null) {
                System.out.println(line);
                result.setText(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
