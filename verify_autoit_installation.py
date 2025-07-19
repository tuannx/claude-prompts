#!/usr/bin/env python3
"""
End-to-end verification of AutoIt support installation
"""
import tempfile
import os


def verify_autoit_installation():
    """Comprehensive verification of AutoIt support"""
    print("=== AutoIt Installation Verification ===")
    
    tests_passed = 0
    total_tests = 5
    
    # Test 1: Import and basic functionality
    print("\nTest 1: Import and basic functionality")
    try:
        from claude_code_indexer.parsers import create_default_parser
        from claude_code_indexer.parsers.autoit_parser import AutoItParser
        from claude_code_indexer.indexer import CodeGraphIndexer
        
        parser = create_default_parser()
        autoit_parser = AutoItParser()
        indexer = CodeGraphIndexer()
        
        print("  PASS: All imports successful")
        tests_passed += 1
    except Exception as e:
        print(f"  FAIL: Import failed - {e}")
    
    # Test 2: Extension support
    print("\nTest 2: Extension support")
    try:
        extensions = parser.get_supported_extensions()
        autoit_exts = [ext for ext in extensions if ext in ['.au3', '.aut', '.a3x']]
        
        if len(autoit_exts) == 3:
            print(f"  PASS: All AutoIt extensions supported: {autoit_exts}")
            tests_passed += 1
        else:
            print(f"  FAIL: Missing extensions. Found: {autoit_exts}")
    except Exception as e:
        print(f"  FAIL: Extension check failed - {e}")
    
    # Test 3: File recognition
    print("\nTest 3: File recognition")
    try:
        can_parse_au3 = parser.can_parse("test.au3")
        can_parse_aut = parser.can_parse("script.aut")
        can_parse_a3x = parser.can_parse("compiled.a3x")
        can_parse_py = parser.can_parse("test.py")  # Should be False for AutoIt parser specifically
        
        if can_parse_au3 and can_parse_aut and can_parse_a3x:
            print("  PASS: AutoIt files recognized correctly")
            tests_passed += 1
        else:
            print(f"  FAIL: File recognition issues - .au3:{can_parse_au3}, .aut:{can_parse_aut}, .a3x:{can_parse_a3x}")
    except Exception as e:
        print(f"  FAIL: File recognition test failed - {e}")
    
    # Test 4: Parsing functionality
    print("\nTest 4: Parsing functionality")
    try:
        autoit_code = '''
#include <GUIConstantsEx.au3>
#include <WindowsConstants.au3>

Global $g_hMainGUI
Global $g_sTitle = "AutoIt Test App"

Func Main()
    Local $hGUI = CreateGUI()
    ShowGUI()
    RunLoop()
EndFunc

Func CreateGUI()
    $g_hMainGUI = GUICreate($g_sTitle, 400, 300)
    Local $idButton = GUICtrlCreateButton("Test Button", 10, 10, 100, 30)
    Return $g_hMainGUI
EndFunc

Func ShowGUI()
    GUISetState(@SW_SHOW, $g_hMainGUI)
EndFunc

Func RunLoop()
    While 1
        Local $msg = GUIGetMsg()
        If $msg = $GUI_EVENT_CLOSE Then ExitLoop
    WEnd
EndFunc

HotKeySet("{F1}", "ShowHelp")

Func ShowHelp()
    MsgBox(0, "Help", "Press F1 for help")
EndFunc

Main()
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.au3', delete=False) as f:
            f.write(autoit_code)
            temp_file = f.name
        
        try:
            result = parser.parse_file(temp_file)
            
            if result.success:
                functions = [n for n in result.nodes.values() if n.node_type == 'function']
                imports = [n for n in result.nodes.values() if n.node_type == 'import']
                variables = [n for n in result.nodes.values() if n.node_type == 'variable']
                gui_controls = [n for n in result.nodes.values() if n.node_type == 'gui_control']
                
                print(f"  Parsed: {len(result.nodes)} nodes, {len(result.relationships)} relationships")
                print(f"  Functions: {len(functions)} ({[f.name for f in functions]})")
                print(f"  Imports: {len(imports)} ({[i.name for i in imports]})")
                print(f"  Variables: {len(variables)}")
                print(f"  GUI Controls: {len(gui_controls)}")
                
                if len(functions) >= 5 and len(imports) >= 2 and len(variables) >= 2:
                    print("  PASS: Parsing successful with expected elements")
                    tests_passed += 1
                else:
                    print("  FAIL: Parsing incomplete - not all elements found")
            else:
                print(f"  FAIL: Parsing failed - {result.error_message}")
                
        finally:
            os.unlink(temp_file)
            
    except Exception as e:
        print(f"  FAIL: Parsing test failed - {e}")
    
    # Test 5: Integration with indexer
    print("\nTest 5: Integration with indexer")
    try:
        # Test that the indexer can use the AutoIt parser
        indexer_can_parse = indexer.parser.can_parse("test.au3")
        
        if indexer_can_parse:
            print("  PASS: Indexer integration working")
            tests_passed += 1
        else:
            print("  FAIL: Indexer cannot parse AutoIt files")
    except Exception as e:
        print(f"  FAIL: Integration test failed - {e}")
    
    # Results
    print(f"\n=== Verification Results ===")
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 SUCCESS: AutoIt support is fully functional!")
        print("\nYou can now use:")
        print("  claude-code-indexer index /path/to/autoit/project")
        print("  claude-code-indexer query --important")
        print("  claude-code-indexer search function_name")
        return True
    else:
        print(f"⚠️  WARNING: {total_tests - tests_passed} test(s) failed")
        print("AutoIt support may not be fully functional.")
        return False


if __name__ == "__main__":
    success = verify_autoit_installation()
    exit(0 if success else 1)