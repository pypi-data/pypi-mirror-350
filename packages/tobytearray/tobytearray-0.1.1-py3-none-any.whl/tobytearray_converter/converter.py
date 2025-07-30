import sys
import gzip
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

@dataclass
class LanguageSpec:
    """Storage for language-specific generation parameters"""
    include: str
    comment: str
    declaration: str
    closing: str
    indent: str = '  '
    bytes_per_line: int = 12

class ResourceConverter:
    def __init__(self, input_file: str, output_file: str, 
                 const_name: Optional[str] = None, compress: bool = True):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.const_name = const_name or self.input_file.stem.lower()
        self.compress = compress
        
        self.language_specs: Dict[str, LanguageSpec] = {
            'cpp': LanguageSpec(
                include='#include <cstdint>',
                comment='//',
                declaration='#define {const_name}_len {length}\nconst uint8_t {const_name}[] = {{',
                closing='};',
                indent='  ',
                bytes_per_line=12
            ),
            'python': LanguageSpec(
                include='',
                comment='#',
                declaration='{const_name} = bytes([',
                closing='])',
                indent='    ',
                bytes_per_line=16
            ),
            'go': LanguageSpec(
                include='',
                comment='//',
                declaration='var {const_name} = []byte{{',
                closing='}',
                indent='    ',
                bytes_per_line=12
            ),
            'rust': LanguageSpec(
                include='',
                comment='//',
                declaration='pub const {const_name}: &[u8] = &[',
                closing='];',
                indent='    ',
                bytes_per_line=12
            )
        }

    def convert(self) -> bool:
        """Main conversion method"""
        try:
            content = self._read_and_compress_file()
            output = self._generate_output(content)
            self._write_output(output)
            print(f"Successfully converted {self.input_file} to {self.output_file}")
            return True
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            return False
        
    def _read_and_compress_file(self) -> bytes:
        """Reading and compressing a file"""
        content = self.input_file.read_bytes()
        return gzip.compress(content) if self.compress else content

    def _get_language_spec(self) -> LanguageSpec:
        """Determining language specification from file extension"""
        ext = self.output_file.suffix.lower()
        return {
            '.cpp': self.language_specs['cpp'],
            '.h': self.language_specs['cpp'],
            '.hpp': self.language_specs['cpp'],
            '.py': self.language_specs['python'],
            '.go': self.language_specs['go'],
            '.rs': self.language_specs['rust']
        }.get(ext, self.language_specs['cpp'])  # default C++

    def _generate_output(self, content: bytes) -> str:
        """Generating output file"""
        spec = self._get_language_spec()
        output: List[str] = []

        output.append(f"{spec.comment} Auto-generated from {self.input_file.name}")
        output.append(f"{spec.include}")
        output.append(f"{spec.comment} Size: {len(content)} bytes")
        
        if self.compress:
            output.append(f"{spec.comment} Content is gzip-compressed")
        
        declaration = spec.declaration.format(
            const_name=self.const_name,
            length=len(content)
        )
        output.append(declaration)
        
        for i in range(0, len(content), spec.bytes_per_line):
            chunk = content[i:i+spec.bytes_per_line]
            hex_bytes = [f'0x{b:02X}' for b in chunk]
            output.append(f"{spec.indent}{', '.join(hex_bytes)},")
        
        output.append(spec.closing)
        
        return "\n".join(output)

    def _write_output(self, output: str) -> None:
        """Write the result to a file"""
        self.output_file.write_text(output)

def convert_file(input_file: str, output_file: str, 
                const_name: Optional[str] = None, compress: bool = True) -> bool:
    """Convenience function for direct use"""
    converter = ResourceConverter(input_file, output_file, const_name, compress)
    return converter.convert()

def main():
    """Command line entry point"""
    if len(sys.argv) < 3:
        print("Usage: resource-converter <input_file> <output_file> [--name CONST_NAME] [--no-compress]")
        sys.exit(1)
    
    args = sys.argv[1:]
    input_file = args[0]
    output_file = args[1]
    const_name = args[args.index('--name') + 1] if '--name' in args else None
    compress = '--no-compress' not in args
    
    if not convert_file(input_file, output_file, const_name, compress):
        sys.exit(1)

if __name__ == "__main__":
    main()