package org.example;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.TextArea;
import javafx.stage.Stage;

import java.io.*;

public class firstController {
    @FXML
    public TextArea phpcode;
    @FXML
    public Button button1;

    public void showResult(ActionEvent actionEvent) throws IOException {
        String codeText = phpcode.getText();
        FileWriter fw;
        try {
            fw = new FileWriter(new File("tanulo_adatok/toimport_vulnerabilities.php"),false);
            fw.write(codeText);
            fw.close();
        } catch (FileNotFoundException e) {
            System.out.println(e.getMessage());
        } catch (IOException e) {
            e.printStackTrace();
        }

        Stage stage = (Stage) button1.getScene().getWindow();
        stage.close();

        Parent root = FXMLLoader.load(getClass().getResource("primary.fxml"));
        Scene scene = new Scene(root);
        stage.setScene(scene);
        stage.show();
    }

}
