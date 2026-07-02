import javax.swing.*;

import java.awt.Color;
import java.awt.Font;
import java.awt.event.*;

public class tempConverter extends JFrame implements ActionListener {

    JTextField inputField;
    JComboBox<String> cbFrom, cbTo;
    JLabel lblResult;
    JButton btnConvert;

    public tempConverter() {

        JLabel lblTemp = new JLabel("Temperature : ");
        lblTemp.setBounds(30, 20, 100, 25);
        add(lblTemp);

        inputField = new JTextField();
        inputField.setBounds(140, 20, 150, 25);
        add(inputField);

        JLabel lblFrom = new JLabel("From:");
        lblFrom.setBounds(30, 60, 100, 25);
        add(lblFrom);

        String[] units = {"Celsius", "Fahrenheit", "Kelvin"};

        cbFrom = new JComboBox<>(units);
        cbFrom.setBounds(140, 60, 150, 25);
        add(cbFrom);

        JLabel lblTo = new JLabel("To:");
        lblTo.setBounds(30, 100, 100, 25);
        add(lblTo);

        cbTo = new JComboBox<>(units);
        cbTo.setBounds(140, 100, 150, 25);
        add(cbTo);

        btnConvert = new JButton("Convert");
        btnConvert.setBounds(140, 140, 100, 30);
        btnConvert.addActionListener(this);
        add(btnConvert);

        lblResult = new JLabel("Result:");
        lblResult.setFont(new Font("Segoe UI", Font.PLAIN, 13));
        lblResult.setForeground(new Color(80, 80, 80));
        lblResult.setBounds(30, 180, 300, 30);
        add(lblResult);

        
        setTitle("Temperature Converter");
        setSize(400, 550);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setVisible(true);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        try {
            double temp = Double.parseDouble(inputField.getText());

            String from = cbFrom.getSelectedItem().toString();
            String to = cbTo.getSelectedItem().toString();

            double result = 
                converterLogic.convert(temp, from, to);

            lblResult.setText(String.format("Result: %.2f", result));
        } catch (NumberFormatException exception) {
            JOptionPane.showMessageDialog(this, "Please Enter a Valid Value!");
        }
    }
}
