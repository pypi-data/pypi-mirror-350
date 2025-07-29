"""
Metadata and branding information for the Pompomp project.

This module centralizes core project information such as
- Logo with color formatting (for CLI display)
- App name, version, description
- Author and contact details
- Licensing and classifiers

It is intended to be imported by CLI or setup tools to maintain consistency.
"""
__logo__ = ("""{{ FRM }}
{{ MP }}                             .          .         {{ P }}        ..          .                             
{{ MP }}                          $+::;x$    $+::;x$      {{ P }}     :X;;;;X+   .$;;;;xX                          
{{ MP }}                        :&&X++X$&&&&&&$x+x$&$.    {{ P }}    ;&$X++X$&&&&&$X++X$&X                         
{{ MP }}                     $$X+$$+++++&+::x$+++++&X+$$X {{ P }}:$$x+Xx++++x$+;;XX++++x&++X$x                     
{{ MP }}                   .$$$X+;x$&&$X+:::;x$&&&X++xX$Xx&&{{ P }}$x++x$&&$x+;;;+x$&&$x++x$$xXx                   
{{ MP }}                   :$:;;x&$$+:::::::::::;x$&$;.....x$+{{ P }}x$$X+;;;;;;;;;;;+X$&x;::::+$                  
{{ MP }}                   :$::::::;X$&X+;:;;x$$X+..........X${{ P }};;;+X$&x+;;;+x&$x;:::::::::x$                 
{{ MP }}                   :$:::::::::;+x$&$x;:.............:$+{{ P }};;;;;;+x$&X+;:::::::::::::;$                 
{{ MP }}                   :$::::::::::::+$;.................$x{{ P }};;;;;;;;+&:::::::::::::::::&                 
{{ MP }}                   :$;:::::::::::+$;.....:;X&&;......&X{{ P }};;;;;;;;+&:::::::+$&x::::::&                 
{{ MP }}                   :&&Xx;::::::::+$;....:$$$X$&.....:$x{{ P }};;;;;;;;+&:::::+&XXX$;:::::$                 
{{ MP }}                   :$:;+$&$x;::::+$;....:$$X$$$.....;&X{{ P }}$$X+;;;;+&:::::+&XX$$;::::+$                 
{{ MP }}                   :$:::::;x$$$+;+$;....:$$$&X......X${{ P }};;;+X$$x+x&:::::+&$$$;:::::X+                 
{{ MP }}                   :$::::::::;;x$&&;....:xx;:......+$+{{ P }};;;;;;;+x$&:::::;X+:::::::+$                  
{{ MP }}                   :$::::::::::::+$;..............+$+{{ P }};;;;;;;;;;+&::::::::::::::+X                   
{{ MP }}                   :$;:::::::::::+$;............;$${{ P }}+;;;;;;;;;;;+&::::::::::::;$;                    
{{ MP }}                   :$$$x+;:::::::+$;.........:x$;{{ P }}x$X$X++;;;;;;;+&:::::::::;x$:                      
{{ MP }}                   :$:;+X&$X;::::+$;.....:X$$:   {{ P }}:$;;;+$$$+;;;;+&::::::x$$.                         
{{ MP }}                   :$:::::;+$$$x;+$;....:$       {{ P }}:$;;;;;;;x$&X+x&:::::+&                            
{{ MP }}                   :$:::::::::;+X$&;....:$       {{ P }}:$;;;;;;;;;;+x$&:::::+&                            
{{ MP }}                   :$::::::::::::+$;....:$       {{ P }}:$;;;;;;;;;;;;+&:::::+&                            
{{ MP }}                   .$;:::::::::::+$;....:$       {{ P }}.$+;;;;;;;;;;;+&:::::+&                            
{{ MP }}                     x$X+;:::::::+$;....:$       {{ P }}  x$x+;;;;;;;;+&:::::+&                            
{{ MP }}                        .$$X+::::+$;..:x$;       {{ P }}      X$X+;;;;+&:::;X$                             
{{ MP }}                            :X$X;+$X$$+          {{ P }}         .X&X+x&x$X.                               
{{ MP }}                                .+;              {{ P }}              ;:                                   
                                                                                                    
       {{ G }};;;;:.   {{ MP }}   :;;;;:     ::      ::   .::::.   {{ P }}   :;;;;:     ::      ::   .::::.            
       {{ G }};;   :;. {{ MP }} :;:    :;:   ;;:    :;;   ::   ::. {{ P }} :;:    :;:   ;;:    :;;   ::   ::.          
       {{ G }};;   :;. {{ MP }}:;:      :;: .;;:;  .;:;.  ::    :. {{ P }}:;:      :;: .;;:;  .;:;.  ::    :.          
       {{ G }};;:;;;:  {{ MP }};;.      .;: .;: :;.;  ;:  :::::::  {{ P }};;.      .;: .;: :;.;  ;:  :::::::           
       {{ G }};;       {{ MP }} ;;.    .;;  :;. .;;.  ;;  ::       {{ P }} ;;.    .;;  :;. .;;.  ;;  ::                
       {{ G }};;       {{ MP }}  :;;;;;;:   :;        ;;  ::       {{ P }}  :;;;;;;:   :;        ;;  ::                
                                                                                                    
""".replace("{{ FRM }}", "[bright_black]")
            .replace("{{ G }}", "[spring_green1]")
            .replace("{{ MP }}", "[medium_purple3]")
            .replace("{{ P }}", "[hot_pink3]"))

__app_name__ = "pompomp"
__version__ = "1.0.1"
__description__ = "Generate sleek, no-fluff themes, tailored for Oh My Posh."
__author__ = "Michel TRUONG"
__email__ = "michel.truong@gmail.com"
__url__ = "https://github.com/KaminoU/pompomp"
__keywords__ = [ "pompomp" ]
__classifiers__ = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.12',
    'Operating System :: OS Independent',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
]
__license_type__ = "MIT"
__license__ = """
MIT License

Copyright © • 2025 • Michel TRUONG

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
