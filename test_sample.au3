#include <GUIConstantsEx.au3>
#include <WindowsConstants.au3>
#include "MyCustomLibrary.au3"

; Sample AutoIt script for testing parser
; This demonstrates various AutoIt features

Global Const $VERSION = "1.0.0"
Global $hGUI, $nMsg
Global $idButton, $idInput, $idLabel

; Main program execution
Main()

Func Main()
    Local $aData[10]
    
    ; Create the GUI
    CreateGUI()
    
    ; Process data
    $aData = GetUserData()
    ProcessData($aData)
    
    ; Show GUI and wait for events
    ShowGUI()
EndFunc

Func CreateGUI()
    Local $nWidth = 300, $nHeight = 200
    
    $hGUI = GUICreate("Sample AutoIt App", $nWidth, $nHeight)
    $idLabel = GUICtrlCreateLabel("Enter your name:", 10, 10, 100, 20)
    $idInput = GUICtrlCreateInput("", 10, 35, 200, 25)
    $idButton = GUICtrlCreateButton("Submit", 10, 70, 80, 30)
    
    GUISetState(@SW_SHOW, $hGUI)
EndFunc

Func ShowGUI()
    While 1
        $nMsg = GUIGetMsg()
        Select
            Case $nMsg = $GUI_EVENT_CLOSE
                ExitLoop
            Case $nMsg = $idButton
                Local $sUserInput = GUICtrlRead($idInput)
                ProcessUserInput($sUserInput)
        EndSelect
    WEnd
    
    GUIDelete($hGUI)
EndFunc

Func GetUserData()
    Local $aData[5] = ["Item1", "Item2", "Item3", "Item4", "Item5"]
    Return $aData
EndFunc

Func ProcessData(ByRef $aInputData)
    For $i = 0 To UBound($aInputData) - 1
        ConsoleWrite("Processing: " & $aInputData[$i] & @CRLF)
    Next
EndFunc

Func ProcessUserInput($sInput)
    If StringLen($sInput) > 0 Then
        MsgBox($MB_ICONINFORMATION, "Hello", "Hello, " & $sInput & "!")
        
        ; Write to registry
        RegWrite("HKEY_CURRENT_USER\Software\MyApp", "LastUser", "REG_SZ", $sInput)
        
        ; Create COM object
        Local $oExcel = ObjCreate("Excel.Application")
        If IsObj($oExcel) Then
            $oExcel.Visible = True
            $oExcel.Quit()
            $oExcel = Null
        EndIf
    Else
        MsgBox($MB_ICONWARNING, "Warning", "Please enter your name!")
    EndIf
EndFunc

; Hotkey function
Func ExitApp()
    Exit
EndFunc

; Set hotkey
HotKeySet("{ESC}", "ExitApp")