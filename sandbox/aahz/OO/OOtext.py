# Can't have blank line at beginning of XML

styles = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE office:document-styles PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "office.dtd">
<office:document-styles xmlns:office="http://openoffice.org/2000/office" xmlns:style="http://openoffice.org/2000/style" xmlns:text="http://openoffice.org/2000/text" xmlns:table="http://openoffice.org/2000/table" xmlns:draw="http://openoffice.org/2000/drawing" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:number="http://openoffice.org/2000/datastyle" xmlns:svg="http://www.w3.org/2000/svg" xmlns:chart="http://openoffice.org/2000/chart" xmlns:dr3d="http://openoffice.org/2000/dr3d" xmlns:math="http://www.w3.org/1998/Math/MathML" xmlns:form="http://openoffice.org/2000/form" xmlns:script="http://openoffice.org/2000/script" office:version="1.0">
 <office:font-decls>
  <style:font-decl style:name="StarSymbol" fo:font-family="StarSymbol" style:font-charset="x-symbol"/>
  <style:font-decl style:name="Courier" fo:font-family="Courier" style:font-family-generic="modern" style:font-pitch="fixed"/>
  <style:font-decl style:name="Arial Unicode MS" fo:font-family="&apos;Arial Unicode MS&apos;" style:font-pitch="variable"/>
  <style:font-decl style:name="Thorndale" fo:font-family="Thorndale" style:font-family-generic="roman" style:font-pitch="variable"/>
 </office:font-decls>
 <office:styles>
  <style:default-style style:family="graphics">
   <style:properties draw:start-line-spacing-horizontal="0.283cm" draw:start-line-spacing-vertical="0.283cm" draw:end-line-spacing-horizontal="0.283cm" draw:end-line-spacing-vertical="0.283cm" fo:color="#000000" style:font-name="Thorndale" fo:font-size="12pt" fo:language="en" fo:country="US" style:font-name-complex="Arial Unicode MS" style:font-size-complex="12pt" style:language-complex="none" style:country-complex="none" style:text-autospace="ideograph-alpha" style:punctuation-wrap="hanging" style:line-break="strict">
    <style:tab-stops/>
   </style:properties>
  </style:default-style>
  <style:default-style style:family="paragraph">
   <style:properties fo:color="#000000" style:font-name="Thorndale" fo:font-size="12pt" fo:language="en" fo:country="US" style:font-name-complex="Arial Unicode MS" style:font-size-complex="12pt" style:language-complex="none" style:country-complex="none" fo:hyphenate="false" fo:hyphenation-remain-char-count="2" fo:hyphenation-push-char-count="2" fo:hyphenation-ladder-count="no-limit" style:text-autospace="ideograph-alpha" style:punctuation-wrap="hanging" style:line-break="strict" style:tab-stop-distance="2.205cm"/>
  </style:default-style>
  <style:style style:name="Standard" style:family="paragraph" style:class="text"/>
  <style:style style:name=".body" style:family="paragraph" style:parent-style-name="Standard"/>
  <style:style style:name=".CALLOUT" style:family="paragraph" style:parent-style-name=".body"/>
  <style:style style:name=".figure" style:family="paragraph" style:parent-style-name=".body"/>
  <style:style style:name=".quotes" style:family="paragraph" style:parent-style-name=".body"/>
  <style:list-style style:name=".bullet"/>
  <style:style style:name=".ch title" style:family="paragraph" style:parent-style-name=".body">
    <style:properties style:font-size="20pt" fo:font-size="20pt"/>
  </style:style>
  <style:style style:name=".head 1" style:family="paragraph" style:parent-style-name=".body">
    <style:properties style:font-size="16pt" fo:font-size="16pt"/>
  </style:style>
  <style:style style:name=".head 2" style:family="paragraph" style:parent-style-name=".body"/>
  <style:style style:name=".code" style:family="paragraph" style:parent-style-name=".body">
   <style:properties style:font-name="Courier"/>
  </style:style>
  <style:style style:name="Footnote Symbol" style:family="text"/>
  <style:style style:name="Bullet Symbols" style:family="text">
   <style:properties style:font-name="StarSymbol" fo:font-size="9pt" style:font-name-complex="StarSymbol" style:font-size-complex="9pt"/>
  </style:style>
  <style:style style:name="Footnote anchor" style:family="text">
   <style:properties style:text-position="super 58%"/>
  </style:style>
  <style:style style:name="code" style:family="text">
   <style:properties style:font-name="Courier"/>
  </style:style>
  <style:style style:name="italic" style:family="text">
   <style:properties fo:font-style="italic"/>
  </style:style>
  <text:outline-style>
   <text:outline-level-style text:level="1" style:num-format=""/>
   <text:outline-level-style text:level="2" style:num-format=""/>
   <text:outline-level-style text:level="3" style:num-format=""/>
   <text:outline-level-style text:level="4" style:num-format=""/>
   <text:outline-level-style text:level="5" style:num-format=""/>
   <text:outline-level-style text:level="6" style:num-format=""/>
   <text:outline-level-style text:level="7" style:num-format=""/>
   <text:outline-level-style text:level="8" style:num-format=""/>
   <text:outline-level-style text:level="9" style:num-format=""/>
   <text:outline-level-style text:level="10" style:num-format=""/>
  </text:outline-style>
  <text:footnotes-configuration style:num-format="1" text:start-value="0" text:footnotes-position="page" text:start-numbering-at="document"/>
  <text:endnotes-configuration style:num-format="i" text:start-value="0"/>
  <text:linenumbering-configuration text:number-lines="false" text:offset="0.499cm" style:num-format="1" text:number-position="left" text:increment="5"/>
 </office:styles>
 <office:automatic-styles>
  <style:page-master style:name="pm1">
   <style:properties fo:page-width="20.999cm" fo:page-height="29.699cm" style:num-format="1" style:print-orientation="portrait" fo:margin-top="2.54cm" fo:margin-bottom="2.54cm" fo:margin-left="3.175cm" fo:margin-right="3.175cm" style:footnote-max-height="0cm">
    <style:footnote-sep style:width="0.018cm" style:distance-before-sep="0.101cm" style:distance-after-sep="0.101cm" style:adjustment="left" style:rel-width="25%" style:color="#000000"/>
   </style:properties>
   <style:header-style/>
   <style:footer-style/>
  </style:page-master>
  <style:page-master style:name="pm2">
   <style:properties fo:page-width="20.999cm" fo:page-height="29.699cm" style:num-format="1" style:print-orientation="portrait" fo:margin-top="2cm" fo:margin-bottom="2cm" fo:margin-left="2cm" fo:margin-right="2cm" style:footnote-max-height="0cm">
    <style:footnote-sep style:adjustment="left" style:rel-width="25%" style:color="#000000"/>
   </style:properties>
   <style:header-style/>
   <style:footer-style/>
  </style:page-master>
 </office:automatic-styles>
 <office:master-styles>
  <style:master-page style:name="Standard" style:page-master-name="pm1"/>
  <style:master-page style:name="Footnote" style:page-master-name="pm2"/>
 </office:master-styles>
</office:document-styles>
'''

manifest = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE manifest:manifest PUBLIC "-//OpenOffice.org//DTD Manifest 1.0//EN" "Manifest.dtd">
<manifest:manifest xmlns:manifest="http://openoffice.org/2001/manifest">
 <manifest:file-entry manifest:media-type="application/vnd.sun.xml.writer" manifest:full-path="/"/>
 <manifest:file-entry manifest:media-type="" manifest:full-path="Pictures/"/>
 %s
</manifest:manifest>
'''

manifest_format = '<manifest:file-entry manifest:media-type="text/xml" manifest:full-path="%s"/>'

content_header = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE office:document-content PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "office.dtd">
<office:document-content xmlns:office="http://openoffice.org/2000/office" xmlns:style="http://openoffice.org/2000/style" xmlns:text="http://openoffice.org/2000/text" xmlns:table="http://openoffice.org/2000/table" xmlns:draw="http://openoffice.org/2000/drawing" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:number="http://openoffice.org/2000/datastyle" xmlns:svg="http://www.w3.org/2000/svg" xmlns:chart="http://openoffice.org/2000/chart" xmlns:dr3d="http://openoffice.org/2000/dr3d" xmlns:math="http://www.w3.org/1998/Math/MathML" xmlns:form="http://openoffice.org/2000/form" xmlns:script="http://openoffice.org/2000/script" office:class="text" office:version="1.0">
 <office:script/>
 <office:font-decls>
  <style:font-decl style:name="Courier" fo:font-family="Courier" style:font-family-generic="modern" style:font-pitch="fixed"/>
  <style:font-decl style:name="Arial Unicode MS" fo:font-family="&apos;Arial Unicode MS&apos;" style:font-pitch="variable"/>
  <style:font-decl style:name="Thorndale" fo:font-family="Thorndale" style:font-family-generic="roman" style:font-pitch="variable"/>
 </office:font-decls>
 <office:automatic-styles/>
 <office:body>
  <text:sequence-decls>
   <text:sequence-decl text:display-outline-level="0" text:name="Illustration"/>
   <text:sequence-decl text:display-outline-level="0" text:name="Table"/>
   <text:sequence-decl text:display-outline-level="0" text:name="Text"/>
   <text:sequence-decl text:display-outline-level="0" text:name="Drawing"/>
  </text:sequence-decls>
'''

content_footer = '''</office:body>
</office:document-content>
'''
