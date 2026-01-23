@echo off
REM GurupiaDict - Complete Workflow Test
REM Tests the entire pipeline with sample data

echo.
echo ================================================================
echo   GurupiaDict - Complete Workflow Demo
echo   연결된 지식, 깨어있는 지혜
echo ================================================================
echo.

REM Step 1: Build Rust Parser
echo [Step 1/4] Building Rust Parser...
echo ----------------------------------------------------------------
cd gurupia-parser
cargo build --release
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Build failed!
    cd ..
    pause
    exit /b 1
)
cd ..
echo ✅ Parser built successfully!
echo.

REM Step 2: Parse Test Data
echo [Step 2/4] Parsing Test Wikipedia XML...
echo ----------------------------------------------------------------
gurupia-parser\target\release\gurupia-parser.exe gurupia-parser\test_wiki.xml test_output.jsonl
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Parsing failed!
    pause
    exit /b 1
)
echo ✅ Parsing completed!
echo.

REM Step 3: Build Knowledge Graph
echo [Step 3/4] Building Knowledge Graph Database...
echo ----------------------------------------------------------------
python gurupia-synthesizer\synthesizer.py test_output.jsonl GurupiaDict_demo.db --reset --stats
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Synthesis failed!
    pause
    exit /b 1
)
echo ✅ Database built successfully!
echo.

REM Step 4: Query Demo
echo [Step 4/4] Running Query Demo...
echo ----------------------------------------------------------------
echo.
echo === Database Statistics ===
python gurupia-synthesizer\query.py GurupiaDict_demo.db --stats
echo.
echo.

echo === Searching for "컴퓨" ===
python gurupia-synthesizer\query.py GurupiaDict_demo.db --search "컴퓨"
echo.
echo.

echo === Viewing "컴퓨터" Article ===
python gurupia-synthesizer\query.py GurupiaDict_demo.db --view "컴퓨터"
echo.
echo.

echo ================================================================
echo   🎉 Complete Workflow Test Finished Successfully!
echo ================================================================
echo.
echo Generated files:
echo   - test_output.jsonl         (JSONL from parser)
echo   - GurupiaDict_demo.db       (SQLite knowledge graph)
echo.
echo Next steps:
echo   1. Download full Wikipedia dump from:
echo      https://dumps.wikimedia.org/kowiki/latest/
echo.
echo   2. Run full pipeline:
echo      parse.bat kowiki-latest-pages-articles.xml wiki_full.jsonl
echo      synthesize.bat wiki_full.jsonl GurupiaDict.db --stats
echo.
echo   3. Query your knowledge graph:
echo      query.bat GurupiaDict.db --interactive
echo.
pause
