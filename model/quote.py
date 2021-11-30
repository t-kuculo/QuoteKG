import re
<<<<<<< HEAD
from transformers import pipeline
model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)


=======
>>>>>>> 8e25dd39d45b7ce7368cf03ad5e5959db5fdd5aa
pattern_brackets = re.compile(r'\[[^\]]*\]') # https://stackoverflow.com/questions/640001/how-can-i-remove-text-within-parentheses-with-a-regex
pattern_brackets2 = re.compile(r'\([^\)]*\)')

pattern_ref = re.compile(r'<ref[^<]*</ref>')
pattern_ref2 = re.compile(r'<ref>[^<]*$')
pattern_ref3 = re.compile(r'<ref[^>]*/>')
pattern_small = re.compile(r'<small[^<]*</small>')
pattern_small2 = re.compile(r'<small>[^<]*$')
pattern_small3 = re.compile(r'<small[^>]*/>')
pattern_multiple_spaces = re.compile(r' +')

def cleanText(text, isQuote=False):
    # remove everything in []
    text = re.sub(pattern_brackets, "", text)
    
    # remove everything in "()" if it is quote text (not in context)
    if isQuote:
        text = re.sub(pattern_brackets2, "", text)

    # remove everything in "<ref"
    text = re.sub(pattern_ref, "", text)
    text = re.sub(pattern_ref2, "", text)
    text = re.sub(pattern_ref3, "", text)
    # remove everything in "<small"
    text = re.sub(pattern_small, "", text)
    text = re.sub(pattern_small2, "", text)
    text = re.sub(pattern_small3, "", text)
    # remove quotation marks at the start and end
    
    if text.endswith('".'):
        text = text[:-2] + '."'
    if text.endswith('».'):
        text = text[:-2] + '.»'

    text = text.strip('\"')
    text = text.strip('\\"')
    text = text.strip('"-”„«»')
    
    # remove any sequences of spaces
    text = re.sub(pattern_multiple_spaces, ' ', text)
    # strip spaces at begin and end
    text = text.strip()
    
    if text == "{{Citace monografie":
        text = None
    
    return text

untemplated = ["eo","en","de","tr","no","hu","ta","he","pt","pl","cy","it","ar","bs","lt","ku","gl","te","hi","sa","sl","hr","sq","sk","ur","sr","eu","el","vi","uz","es","id","th","az","li","kn","ja","si"]
templated = ["fr","da","nl","be","is","ca","bg","da","ka"] +["zh"]
hybrid = ["uk","ru","sv","et"] + ["ko","fa","cs","fi", "hy"]

forbidden_non_alphanumerics_for_context = ["{","}",">","<","@","+","#","&","˛","ˇ","^","`","˙","´","˝","¸"]
forbidden_non_alphanumerics_for_quotes = forbidden_non_alphanumerics_for_context+["[", "]"]


<<<<<<< HEAD
misattributed_dict = {
    'ar': ['ضعيف', 'متنازع عليه', 'بشكل غير صحيح', 'قائلا نعزى خطأ', 'يعزى خطأ إلى', 'ونقلت تم تعيينها', 'إساءة', 'نعزى بشكل غير صحيح', 'متصل بشكل غير صحيح', 'يعزى بشكل غير صحيح إلى', 'مثيرة للجدل', 'تم تعيينه بشكل غير صحيح', 'تم تعيينه بشكل غير صحيح', 'الفضل بشكل غير صحيح', 'مشكوك فيه', 'سوء المعاملة', 'سيئة', 'خاطئ', 'الفضل بشكل خاطئ', 'لم يتم التحقق منه', 'مرفقة بشكل غير صحيح', 'الفضل بشكل غير صحيح', 'غير صحيح', 'يعزى إلى الخطأ', 'مشبوه أو مشكوك فيه'],\
    'az': ['zəif', 'mübahisəli', 'yanlış', 'yanlış şəkildə aid olduğunu söyləmək', 'səhv yanına aiddir', 'Təyin olunmuş sitatlar', 'yanılsaq', 'səhv aiddir', 'səhv bağlıdır', 'səhv aiddir', 'mübahisəli', 'səhv təyin olunur', 'səhv təyin olunmuşdur', 'səhv hesablanır', 'şübhəli', 'rəfiqə', 'zəif', 'səhv', 'səhv hesablanır', 'təsdiqlənməmiş', 'səhv əlavə olunur', 'səhv hesablanır', 'yanlış', 'səhvən aiddir', 'şübhəli'],\
    'be': ['слабы', 'спрэчны', 'няправільна', 'кажучы няправільна прыпісаны', 'памылкова звязаны з', 'Цытаты прызначаныя', 'misatributed', 'няправільна прыпісваецца', 'няправільна падлучаны', 'няправільна прыпісваецца', 'супярэчлівы', 'няправільна прызначаны', 'няправільна прызначаны', 'залічваецца няправільна', 'няпэўны', 'адварочваў', 'кепска', 'памылковы', 'памылкова залічана', 'неўверыў', 'няправільна прыкладаецца', 'няправільна залічаны', 'няправільны', 'прыпісваецца памылкова', 'падазроны'],\
    'bg': ['слаб', 'оспорван', 'неправилно', 'казвайки погрешно приписване', 'погрешно се приписва', 'цитати', 'Misattributed.', 'неправилно приписано', 'неправилно свързани', 'неправилно', 'противоречиви', 'е неправилно назначен', 'неправилно зададен', 'кредитирани неправилно', 'съмнително', 'Млъкни', 'лошо', 'погрешно', 'неправилно кредитирани', 'Несъвършен', 'неправилно прикрепени', 'неправилно кредитирани', 'неправилен', 'се приписва на погрешно', 'подозрителен'],\
    'bs': ['slab', 'sporan', 'pogrešno', 'govoreći pogrešno pripisano', 'pogrešno se pripisuje', 'Citati dodijeljene', 'misao', 'Netačno pripisan', 'Nepravilno povezani', 'pogrešno pripisan', 'kontroverzan', 'pogrešno je dodeljen', 'pogrešno dodijeljeno', 'pripisuju pogrešno', 'sumnjiv', 'maltretiran', 'slabo', 'pogrešno', 'pogrešno pripisan', 'neprovjeren', 'pogrešno priložen', 'pogrešno pripisan', 'netačan', 'pripisuje se pogrešno', 'sumnjiv'], \
    'ca': ['feble', 'en disputa', 'incorrectament', 'dient incorrectament atribuït', "s'atribueix incorrectament a", 'Cotitzacions assignades', 'Misattributed', 'atribuïts incorrectament', 'connectat incorrectament', 'atribuït incorrectament a', 'controvertit', 'està assignat incorrectament', 'assignat incorrectament', 'acreditat incorrectament', 'dubtós', 'maltractat', 'pobrament', 'mal', 'acreditat incorrectament', 'no verificat', 'incorrectament adjunt', 'acreditat incorrectament', 'incorrecte', "s'atribueix a erròniament", 'sospitós'], \
    'co': ['debuli', 'disputa', 'sbagliatu', 'dicendu attribuitu sbagliatu', 'sbagliatu hè attribuita à', 'Quotes assignati', 'misattribuitu', 'attribuitu sbagliatu', 'cunnessu sbagliatu', 'attribuitu sbagliatu à', 'cuntruversuale', 'hè incorrectamente assignatu', 'assignatu sbagliatu', 'creditu sbagliatu', 'dubbitu', 'MISTORATU', 'Poviru', 'sbagliatu', 'sbagliatu creditu', 'Unvererazionatu', 'sbagliatu attaccatu', 'incorrectamente creditu', 'sbagliatu', 'hè attribuita à sbaglià', 'suspicosu'],\
    "cs": ['pochybný', 'nesprávně je připisován', 'je přičítán omylem', 'neosgejavané.', 'říká se nesprávně přiřazené', 'sporný', 'je nesprávně přiřazen', 'špatně', 'nesprávně připojeno', 'nesprávně', 'nezbytný', 'nesprávně přiřazeno', 'nesprávně přisuzováno', 'špatně zacházený', 'slabý', 'nesprávný', 'nesprávně připsány', 'nesprávně připsaný', 'přidělené nabídky', 'podezřelý', 'neověřené'],\
    'da': ['svag', 'bestridt', 'forkert', 'siger fejlagtigt tilskrevet', 'fejlagtigt tilskrives', 'citater tildelt', 'misattributed.', 'forkert tilskrevet', 'forkert forbundet', 'forkert tilskrives', 'kontroversielt', 'er forkert tildelt', 'forkert tildelt', 'krediteret forkert', 'tvivlsom', 'mishandlet', 'Dårlig', 'forkert', 'fejlagtigt krediteret', 'unverified.', 'forkert vedhæftet', 'forkert krediteret', 'ukorrekt', 'er tilskrevet fejlagtigt', 'mistænksom'], \
    "de": ['falsch verbunden', 'falsch angebracht', 'falsch zugewiesen', 'wird fehlerhaft zurückgeführt', 'schwach', 'fälschlich zugeschrieben', 'falsch zugerechnet', 'falsch wird zugeschrieben', 'falsch', 'falsch angeschlossen', 'misshandelt', 'unrecht zugeschrieben werden', 'misstrauisch', 'falsch gutgeschrieben', 'zweifelhaft', 'ist falsch zugewiesen', 'notwendig', 'zitate zugewiesen', 'nicht verifiziert'],\
    'el': ['αδύναμος', 'αμφισβητούμενος', 'εσφαλμένα', 'λέγοντας εσφαλμένα αποδόσεις', 'λανθασμένα αποδίδεται σε', 'αποσπάσματα', 'απροσδόκητος', 'που αποδίδονται εσφαλμένα', 'εσφαλμένα συνδεδεμένο', 'που αποδοθεί εσφαλμένα', 'αμφιλεγόμενος', 'έχει ανατεθεί εσφαλμένα', 'εσφαλμένα αποδίδεται', 'πιστώθηκε λανθασμένα', 'αμφίβολος', 'κακομεταχειρίζομαι', 'πτωχώς', 'λανθασμένος', 'λάθος πιστώθηκε', 'ανεπιβεβαίωτος', 'Επισυνάπτεται εσφαλμένα', 'εσφαλμένα πιστώνεται', 'ανακριβής', 'αποδίδεται λανθασμένα', 'ύποπτος'],\
    "en": ['weak', 'disputed', 'incorrectly', 'saying wrongly attributed', 'wrongly is attributed to', 'quotes assigned', 'misattributed', 'incorrectly attributed', 'incorrectly connected', 'incorrectly attributed to', 'controversial', 'is incorrectly assigned', 'incorrectly assigned', 'credited incorrectly', 'doubtful', 'mistreated', 'poorly', 'wrong', 'wrongly credited', 'unverified', 'incorrectly attached', 'incorrectly credited', 'incorrect', 'is attributed to mistakenly', 'suspicious'],\
    "es": ['débil', 'disputado', 'incorrectamente', 'decir atribuido incorrectamente', 'atribuido incorrectamente a', 'citas asignadas', 'atribuido incorrectamente', 'atribuido incorrectamente', 'conectado incorrectamente', ' atribuido incorrectamente a ',' controvertido ',' asignado incorrectamente ',' asignado incorrectamente ',' acreditado incorrectamente ',' dudoso ',' maltratado ',' mal ',' incorrecto ',' acreditado incorrectamente ',' no verificado ', 'adjunto incorrectamente', 'acreditado incorrectamente', 'incorrecto', 'atribuido erróneamente', 'sospechoso'],\
    'et': ['nõrk', 'vaidlustatud', 'valesti', 'öeldes valesti omistatud', 'valesti omistatakse', 'määratud hinnapakkumisi', 'eksima', 'valesti omistatud', 'valesti ühendatud', 'valesti omistatud', 'vastuoluline', 'on valesti määratud', 'valesti määratud', 'krediteeritud valesti', 'kahtlane', 'väärkohtlemine', 'halvasti', 'vale', 'valesti krediteeritud', 'vastamata jätmine', 'valesti kinnitatud', 'valesti krediteeritud', 'vale', 'omistatakse ekslikult', 'kahtlane'],\
    'eu': ['ahul', 'jokatu', 'gaizki', 'gaizki egozten esanda', 'gaizki egozten zaio', 'esleitutako aipuak', 'Misattributatua', 'oker egotzi', 'Gaizki konektatuta', 'oker egotzita', 'Polemika', 'gaizki esleitzen da', 'gaizki esleituta', 'oker kreditua', 'zalantzazko', 'tratu txarrak', 'txarto', 'okerreko', 'gaizki kreditatu', 'irentetu gabe', 'oker erantsita', 'Gaizki kreditatu', 'ez zuzen', 'oker egozten zaio', 'goganbehartsu'],\
    'fa': ['ضعیف', 'متضاد', 'نادرست', 'گفتن اشتباه است', 'اشتباه به آن نسبت داده می شود', 'نقل قول اختصاص داده شده', 'سوء تفاهم', 'نادرست نسبت داده شده است', 'نادرست متصل است', 'نادرست به', 'بحث برانگیز', 'نادرست اختصاص داده شده است', 'اشتباه اختصاص داده شده است', 'اعتبار نادرست', 'مشکوک', 'بدرفتاری', 'ضعیف', 'اشتباه', 'اشتباه اعتبار', 'غیر قابل تایید', 'اشتباه متصل شده', 'اشتباه اعتبار', 'غلط', 'به اشتباه نسبت داده شده است', 'مشکوک'],\
    'fi': ['heikko', 'kiistanalainen', 'väärin', 'sanomalla väärin', 'virheellisesti johtuu', 'Lainaukset', 'huonosti', 'virheellisesti', 'Väärin kytketty', 'virheellisesti', 'kiistanalainen', 'on asetettu virheellisesti', 'Virheellisesti määritetty', 'hyvitetään väärin', 'epäilyttävä', 'kohteliaisuus', 'huonosti', 'väärä', 'Väärin hyvitetty', 'vahvistettu', 'Virheellisesti kiinnitetty', 'Virheellisesti hyvitetty', 'väärä', 'johtuu virheellisesti', 'epäilyttävä'],\
    'fr': ['faible', 'contesté', 'incorrectement', 'dire attribué à tort', 'est attribué à tort à', 'citations attribuées', 'mal attribué', 'mal attribué', 'incorrectement connecté', ' attribué à tort à', 'controversé', 'est attribué de manière incorrecte', 'attribué de manière incorrecte', 'crédité de manière incorrecte', 'douteux', 'maltraité', 'mal', 'mauvais', 'crédité à tort', 'non vérifié', 'incorrectement joint', 'mal crédité', 'incorrect', 'est attribué à tort', 'suspect'],\
    'he': ['חלש', 'משווקת', 'לא נכון', 'אומר מיוחסת בטעות', 'בטעות מיוחסת', 'ציטוטים שהוקצו', 'misattributed', 'המיוחס בצורה שגויה', 'קשור באופן שגוי', 'המיוחס לא נכון', 'שנוי במחלוקת', 'מוקצה באופן שגוי', 'שהוקצו באופן שגוי', 'זוכה באופן שגוי', 'מוטל בספק', 'התעללות', 'גרוע', 'שגוי', 'שזוכו בטעות', 'unverified', 'המצורפת באופן שגוי', 'זוכה לא נכון', 'לֹא נָכוֹן', 'מיוחסת לטעות בטעות', 'חָשׁוּד'], 'hi': ['कमज़ोर', 'विवादित', 'गलत तरीके से', 'गलत तरीके से कहना', 'गलत तरीके से जिम्मेदार है', 'उद्धरण सौंपा', 'गलत', 'गलत तरीके से जिम्मेदार', 'गलत तरीके से जुड़ा हुआ', 'गलत तरीके से जिम्मेदार ठहराया', 'विवादास्पद', 'गलत तरीके से सौंपा गया है', 'गलत तरीके से असाइन किया गया', 'गलत तरीके से श्रेय दिया गया', 'संदिग्ध', 'दुराचारित', 'बीमार', 'गलत', 'गलत तरीके से श्रेय दिया गया', 'असत्यापित', 'गलत तरीके से संलग्न', 'गलत तरीके से श्रेय दिया गया', 'ग़लत', 'गलती से जिम्मेदार है', 'संदेहजनक'],\
    'hr': ['slab', 'osporen', 'nepravilno', 'govoreći pogrešno pripisuje se', 'pogrešno se pripisuje', 'dodijeljeni citati', 'pogrešan', 'Neispravno se pripisuje', 'pogrešno povezan', 'pogrešno pripisuje', 'kontroverzno', 'je pogrešno dodijeljen', 'pogrešno dodijeljen', 'pogrešno pripisano', 'sumnjiv', 'maltretiran', 'slabo', 'pogrešno', 'pogrešno pripisano', 'neveritičan', 'pogrešno pričvršćen', 'pogrešno pripisano', 'netočno', 'se pripisuje pogrešno', 'sumnjičav'],\
    'hu': ['gyenge', 'vitatott', 'tévesen', 'rosszul mondván', 'helytelenül tulajdonítható', 'Idézetek hozzárendeltek', 'félreérthetetlen', 'helytelenül tulajdonítható', 'Helytelenül csatlakoztatva van', 'helytelenül tulajdonítható', 'vitatott', 'helytelenül hozzárendelt', 'Helytelenül hozzárendelt', 'helytelenül jóváírják', 'kétséges', 'rosszul kezelt', 'rosszul', 'rossz', 'tévesen jóváírta', 'ellenőrizetlen', 'Helytelenül csatolt', 'helytelenül jóváírta', 'helytelen', 'tévesen tulajdonítható', 'gyanús'],\
    'hy': ['թույլ', 'վիճված', 'սխալ', 'սխալ ասելով, վերագրվում է', 'սխալ է վերագրվում', 'Նշված մեջբերումները', 'Մատսել է', 'Սխալ կերպով վերագրվում է', 'Սխալ միացված', 'սխալ է վերագրվել', 'վիճաբանական', 'սխալ է նշանակվել', 'Սխալ նշանակված', 'սխալվել է սխալ', 'կասկածելի', 'չարամտել', 'վատ', 'սխալ', 'սխալվել է', 'անավարտ', 'Սխալորեն կցված', 'սխալ է գնահատվել', 'սխալ', 'վերագրվում է սխալմամբ', 'կասկածելի'],\
    'id': ['lemah', 'diperdebatkan', 'salah', 'mengatakan salah dikaitkan.', 'salah dikaitkan dengan', 'Kutipan ditugaskan', 'salah penyibaran', 'salah dikaitkan', 'salah terhubung', 'salah dikaitkan dengannya', 'kontroversial', 'salah ditugaskan', 'salah ditugaskan', 'dikreditkan secara salah', 'diragukan lagi', 'Dianiaya', 'buruk', 'salah', 'salah dikreditkan', 'tidak diverifikasi', 'salah melekat', 'salah dikreditkan', 'salah', 'dikaitkan dengan keliru', 'mencurigakan'],\
    'is': ['veik', 'umdeildur', 'rangt', 'segja að ranglega rekja til', 'rangt stafar af', 'Tilvitnanir úthlutað', 'misertributed.', 'rangt rekja má', 'rangt tengt', 'rangt rekja til', 'umdeild', 'er rangt úthlutað', 'rangt úthlutað', 'lögð rangt', 'efast', 'mistreated.', 'illa', 'rangt', 'ranglega lögð inn', 'unverfied.', 'rangt fylgir', 'Rangt viðurkennt', 'rangt', 'er rekja til ranglega', 'grunsamlegt'],\
    'it': ['debole', 'disputato', 'erroneamente', 'detto erroneamente attribuito', 'erroneamente attribuito a', 'virgolette assegnate', 'erroneamente attribuito', 'erroneamente attribuito', 'erroneamente connesso', ' erroneamente attribuito a', 'controverso', 'è assegnato in modo errato', 'assegnato in modo errato', 'accreditato in modo errato', 'dubbio', 'maltrattato', 'male', 'sbagliato', 'accreditato erroneamente', 'non verificato', 'erroneamente allegato', 'erroneamente accreditato', 'errato', 'è attribuito a erroneamente', 'sospetto'],\
    'ja': ['弱い', '議論した', '誤って', '間違って帰ったことを言っています', '間違って帰属しています', '割り当てられた引用符', '誤動作しました', '間違って帰属しました', '誤って接続されています', '誤って帰属しました', '物議を醸す', '間違って割り当てられています', '間違って割り当てられています', '誤って入金されました', '疑わしい', '虐待された', '不完全に', '間違い', '間違ってクレジットされました', '未検証', '誤って添付されています', '誤ってクレジットされました', '正しくない', '誤って帰属されています', '疑わしい'],\
    'ka': ['სუსტი', 'სადავო', 'არასწორად', 'არასწორად მიეკუთვნება', 'არასწორად მიეკუთვნება', 'შეთავაზებები', 'misattributed', 'არასწორად მიეკუთვნება', 'არასწორად უკავშირდება', 'არასწორად მიეკუთვნება', 'დროებითი', 'არასწორად არის მინიჭებული', 'არასწორად მინიჭებული', 'არასწორად დაკრედიტდება', 'საეჭვო', 'mistreated', 'ღარიბად', 'მცდარი', 'არასწორად დაკრედიტდება', 'გადაუსებული', 'არასწორად ერთვის', 'არასწორად დაკრედიტდება', 'არასწორი', 'შეცდომით მიეკუთვნება', 'საეჭვო'],\
    'ko': ['약한', '분쟁', '틀리게', '잘못된 것으로 말하고있다', '잘못된 것은', '할당 된 따옴표', '미해시', '잘못된 것으로 잘못된 것입니다', '잘못 연결되었습니다', '잘못된 것으로 잘못된 것입니다', '논란이 많은', '잘못 지정됩니다', '잘못 지정되었습니다', '잘못 적립되었습니다', '불안한', '학대하다', '신통치 않게', '잘못된', '잘못된 적립 된 것', '확인되지 않았습니다', '잘못 첨부되었습니다', '잘못 적립되었습니다', '잘못된', '실수로 기인합니다', '의심스러운'],\
    'lt': ['Silpnas', 'ginčijama', 'Neteisingai', 'sakydamas neteisingai priskirtas', 'neteisingai priskiriama', 'Citatos', 'nesuderinta', 'neteisingai priskiriama', 'neteisingai prijungta', 'neteisingai priskirta', 'prieštaringas', 'yra neteisingai priskirtas', 'neteisingai priskirtas', 'neteisingai įskaityta', 'abejotina', 'netinkamai elgiamasi', 'blogai', 'neteisingas', 'neteisingai įskaityta', 'nepatvirtinta', 'neteisingai prijungtas', 'neteisingai įskaityta', 'Neteisinga', 'priskiriama klaidingai', 'įtartinas'],\
    'nl': ['zwak', 'twijfelachtig', 'onjuist', 'Samenstellen ten onrechte toegeschreven', 'ten onrechte wordt toegeschreven aan', 'Citaten toegewezen', 'verkeerd ingesteld', 'Onjuist toegeschreven', 'Onjuist aangesloten', 'onjuist toegeschreven aan', 'controverseel', 'is verkeerd toegewezen', 'Onjuist toegewezen', 'verkeerd gecrediteerd', 'twijfelachtig', 'mishandeld', 'slecht', 'mis', 'ten onrechte gecrediteerd', 'ongehroken', 'verkeerd bevestigd', 'onjuist gecrediteerd', 'niet correct', 'wordt toegeschreven aan ten onrechte', 'verdacht'],\
    'no': ['svak', 'omstridt', 'feil', 'sier feilaktig tilskrives det', 'feil er tilskrevet', 'Sitater tildelt', 'misattributed.', 'feilaktig tilskrives det', 'feil tilkoblet', 'feilaktig tilskrives', 'kontroversiell', 'er feil tildelt', 'feilaktig tildelt', 'krediteres feil', 'tvilsom', 'feilbehandlet', 'dårlig', 'feil', 'feil kreditert', 'unverified.', 'feil festet', 'feil kreditert', 'stemmer ikke', 'er tilskrevet feilaktig', 'mistenkelig'],\
    'ro': ['slab', 'contestată', 'incorect', 'spunând atribuit greșit', 'este atribuit în mod greșit', 'Citate atribuite', 'misattribuit', 'incorect atribuită', 'incorect conectat', 'incorect atribuită', 'controversat', 'este atribuită incorect', 'incorect atribuite', 'creditat incorect', 'îndoielnic', 'maltratat', 'slab', 'gresit', 'creditat greșit', 'neveriectificat', 'În mod incorect atașat', 'incorect creditate', 'incorect', 'este atribuită în mod eronat', 'suspicios'],\
    'ru': ['слабый', 'оспариваемый', 'неправильно', 'говорить неправильно приписанным', 'неправильно объясняется', 'цитаты назначены', 'несущественно', 'неправильно приписан', 'неправильно подключен', 'неправильно приписан', 'спорный', 'неверно назначен', 'неверно назначен', 'зачислен неправильно', 'сомнительный', 'плохо обращаться', 'плохо', 'неправильный', 'неправильно приписывать', 'неверно', 'неправильно прилагается', 'неправильно зачислено', 'неверный', 'приписывается по ошибке', 'подозрительный'],\
    'sk': ['slabý', 'sporný', 'nesprávne', 'hovorí nesprávne pripisované', 'nesprávne sa pripisuje', 'Pridelené citácie', 'nesprávny', 'Nesprávne pripísané', 'Nesprávne pripojené', 'nesprávne pripísané', 'kontroverzný', 'je nesprávne priradený', 'Nesprávne priradené', 'nesprávne pripísané', 'pochybný', 'nespokojný', 'úboho', 'vhodný', 'nesprávne pripísané', 'neoverený', 'Nesprávne pripojené', 'Nesprávne pripísané', 'nesprávny', 'sa pripisuje mylne', 'podozrivý'],\
    "sl": ["neozdrojované"'napačno prijavljeno', 'rekel napačno pripisano', 'napačno nakazana', 'napačno povezan', 'slabo', 'sumljivega', 'nepravilno dodeljena', 'neosgejavan.', 'dodeljeni citati', 'sporno', 'nepravilno pritrjena', 'nepreverjeno', 'napačno', 'je nepravilno dodeljen', 'nepravilno', 'napačno pripisano', 'se pripisuje pomotoma', 'in pavipe.', 'napačno pripisuje', 'dvomljiv', 'šibko', 'narobe', 'nepravilno pripisana'],\
    "sq": ['i diskutueshëm', 'atribuohet gabimisht', 'i keqtrajtuar', 'i atribuohet gabimisht', 'i pasaktë', 'kredituar gabimisht', 'caktohet gabimisht', 'i lidhur gabimisht', 'i dyshimtë', 'i pavepi', 'i gabuar', 'thënie të atribuara gabimisht', 'bashkangjitur gabimisht', 'dobet'],\
    "pl": ['zło', 'błędny', 'misattriruted.', 'źle traktować', 'słabo', 'wątpliwy', 'nieprawidłowo przymocowany', 'nieprawidłowo przypisany do', 'niepoprawnie przypisany', 'niepoprawnie połączony', 'mówiąc błędnie przypisany', 'kwestionować', 'cytaty przypisywane', 'niesprawdzony', 'błędnie przypisany', 'nieprawidłowo przypisany'], \
    'pt': ['fraca', 'contestada', 'incorretamente', 'dizendo atribuída incorretamente', 'atribuída incorretamente a', 'citações atribuídas', 'atribuída incorretamente', 'atribuída incorretamente', 'conectada incorretamente', ' atribuído incorretamente a ',' controverso ',' atribuído incorretamente ',' atribuído incorretamente ',' creditado incorretamente ',' duvidoso ',' maltratado ',' mal ',' errado ',' creditado incorretamente ',' não verificado ', 'incorretamente anexado', 'incorretamente creditado', 'incorreto', 'atribuído a incorretamente', 'suspeito'], \
    'ta': ['பலவீனமான', 'விவாதத்திற்குரியது', 'தவறாக', 'தவறாக சொல்லப்பட்டது', 'தவறாக காரணம்', 'மேற்கோள் ஒதுக்கப்படும்', 'misattributed.', 'தவறாக காரணம்', 'தவறாக இணைக்கப்பட்டுள்ளது', 'தவறாக காரணம்', 'சர்ச்சைக்குரிய', 'தவறாக ஒதுக்கப்பட்டுள்ளது', 'தவறாக ஒதுக்கப்படும்', 'தவறாக வழங்கப்பட்டது', 'சந்தேகம்', 'தவறாக நடத்தப்பட்டது', 'மோசமாக', 'தவறு', 'தவறாக வரவு', 'சரிபார்க்கப்படவில்லை', 'தவறாக இணைக்கப்பட்டுள்ளது', 'தவறாக நம்பப்படுகிறது', 'தவறானது', 'தவறுதலாக காரணம்', 'சந்தேகத்திற்கிடமான'],\
    'te': ['బలహీనమైన', 'వివాదాస్పదంగా', 'తప్పుగా', 'తప్పుగా ఆపాదించబడినది', 'తప్పుగా ఆపాదించబడినది', 'కేటాయించిన కోట్స్', 'myatattributed', 'తప్పుగా ఆపాదించబడినది', 'తప్పుగా కనెక్ట్ చేయబడింది', 'తప్పుగా ఆపాదించబడినది', 'వివాదాస్పద', 'తప్పుగా కేటాయించబడుతుంది', 'తప్పుగా కేటాయించబడింది', 'తప్పుగా జమ చేయబడుతుంది', 'అనుమానాస్పద', 'బాధితుడు', 'పేలవంగా', 'తప్పు', 'తప్పుగా ఘనత పొందింది', 'ధృవీకరించనిది', 'తప్పుగా జతచేయబడింది', 'తప్పుగా ఘనత పొందింది', 'తప్పు', 'తప్పుగా ఆపాదించబడింది', 'అనుమానాస్పద'],\
    'uk': ['слабкий', 'спірний', 'неправильно', 'кажучи неправильно віднесено', 'неправильно пояснюється', 'Призначені цитати', 'мізерний', 'неправильно віднесено', 'неправильно підключено', 'неправильно віднесено', 'суперечливий', 'неправильно призначено', 'неправильно призначено', 'неправильно приписується', 'сумнівний', 'погано', 'погано', 'неправильний', 'неправильно зарахований', 'неперевірений', 'неправильно прикріплені', 'неправильно зараховано', 'неправильний', 'пояснюється помилково', 'підозрілий'],\
    'ur': ['کمزور', 'متنازعہ', 'غلط طور پر', 'غلط طور پر منسوب کیا گیا ہے', 'غلط طور پر منسوب کیا جاتا ہے', 'حوالہ جات', 'غلط استعمال کی اطلاع دیتے ہوئے ایرر آ گیا ہے', 'غلط طور پر منسوب', 'غلط طور پر منسلک', 'غلط طور پر منسوب', 'متضاد', 'غلط طور پر تفویض کیا جاتا ہے', 'غلط طور پر تفویض', 'غلط طریقے سے کریڈٹ', 'شکست', 'غلطی', 'غریب', 'غلط', 'غلط طور پر کریڈٹ', 'غیر تصدیق شدہ', 'غلط طریقے سے منسلک', 'غلط طریقے سے کریڈٹ', 'غلط', 'غلطی سے منسوب کیا جاتا ہے', 'مشکوک'],\
    'vi': ['Yếu', 'tranh chấp', 'không chính xác', 'nói sai quy kết', 'sai được quy cho', 'Báo giá được giao', 'sai lệch', 'quy cho không chính xác', 'kết nối không chính xác', 'quy cho không chính xác cho.', 'gây tranh cãi', 'được giao không chính xác', 'chỉ định không chính xác', 'ghi có không chính xác', 'nghi ngờ', 'ngược đãi', 'kém', 'Sai lầm', 'Tín dụng sai', 'chưa được xác minh', 'đính kèm không chính xác', 'Credited không chính xác', 'không đúng', 'được quy cho nhầm', 'khả nghi'],\
    'zh': ['弱', '有争议', '不正确', '错误归因', '错误归因于', '引用分配', '错误归因', '错误归因', '错误连接', ' 错误地归因于', '有争议的', '被错误地分配', '错误地分配','记入错误','可疑','虐待','差','错误','错误记入','未验证', '错误附加','错误记入','错误','归因于错误','可疑']
}


misattributed = [f.lower() for l in list(misattributed_dict.values()) for f in l]
=======
misattributed = ["misattributed","Nesprávně přisuzováno","disputed",\
"Thënie të atribuara gabimisht","fälschlich zugeschrieben","zweifelhaft"]

>>>>>>> 8e25dd39d45b7ce7368cf03ad5e5959db5fdd5aa
about = {"en":"quotes about ","de":"zitate mit bezug auf ","fr":"sur ","it":"citazioni su ", "es":"sobre ","nl":"over ", "pl":"o ",\
"ru":"Об ","pt":"sobre","be":"Выказванні пра ","uk":"Про ","ca":"citacions sobre ","hu":"róla mondták",\
"fi":"sanottua","he":"נאמר עליו","fa":"دربارهٔ او","ko":"관련 어록","tr":"Hakkında","sq":"Thënie për të", "ar" : "اقتباسات عن",\
"ro":"despre ", "cs":"ve výrocích"}

about_list = ["quotes about ", "zitate mit bezug auf ", "Ve výrocích","quotes about ","zitate mit bezug auf ","sur ",\
"citazioni su ", "sobre ","Об ","Выказванні пра ","Про ","citacions sobre ","róla mondták","sanottua","נאמר עליו","دربارهٔ او","관련 어록",\
"Hakkında","Thënie për të", ]


attrDict = {
    "bron" : "source","aangehaald" : "cited","taal" : "language","opmerking" : "comment","tekst" : "quote","vertaling" : "translation",
    "نویسنده" : "author",
    "simple" : "quote",
    "ციტატა" : "quote",
    "original": "original","citation": "translation","précisions": "comment","langue": "language","date":"date","parution":"release","source":"source",

    "1":"quote", # Make it work when there are more numbers!!
    "2":"quote",
    "3":"quote",
    "4":"quote",
    "5":"quote",
    "6":"quote",
    "7":"quote",
    "8":"quote",
    "9":"quote",
    "10":"quote",

    "작성일자":"date","제목":"title","출판사":"publisher","url":"url",
    "překladatelé":"translators",
    "titul":"title","příjmení":"surname","místo":"location","isbn":"isbn","vydavatel":"publisher","jméno":"name","rok":"year", "datum přístupu":"access_date","datum vydání":"release_date","issn":"issn",
    "periodikum":"periodical","měsíc":"month","strany":"page",
    "Цитата":"quote","Автор":"author","Коментар":"comment",
    "Комментарий":"comment","Original":"original",
    "Каментар":"comment","Цытата":"quote","Аўтар":"author","крыніца":"source",
    "Tekijä":"author","Viitattu":"referenced","Osoite":"address","Julkaisu":"publication","Nimeke":"title","Ajankohta":"date",
    "útskýring":"explanation", "language":"language","frummál":"quote",
    "cita":"quote","data":"date","lloc":"location","idioma":"language","notes":"notes",
    "editor":"editor","year":"year","publisher":"publisher","page":"page","title":"title","ISBN":"isbn", 
    "archive-date":"archive_date","accessdate":"access_date","archive-url":"archive_url","title":"title","archive_date":"achive:date","access-date":"access_date"
}           
<<<<<<< HEAD




=======
>>>>>>> 8e25dd39d45b7ce7368cf03ad5e5959db5fdd5aa
#from googletrans import Translator
from model.line import *
#translator = Translator()
#from nltk.sentiment import SentimentIntensityAnalyzer   
from sentence_transformers import SentenceTransformer
import langdetect
from langdetect import detect
from dateparser import *
ddp = DateDataParser()


#sia = SentimentIntensityAnalyzer()
def isDate(text):
    X= text.split(" ")
    t = ddp.get_date_tuple(text)
    date = None
    if t.date_obj:
        period = t.period
        if period == "day":
            date = (t.date_obj.year, t.date_obj.month, t.date_obj.day)
        elif period == "month":
            date = (t.date_obj.year, t.date_obj.month)
        elif period == "year":
            date = (t.date_obj.year)
    if any(X):
        date = isDate(" ".join(X[1:]))
    return date

def getDate(section_titles):
    # take the last date 
    # print("TITLES: ", len(section_titles))
    date = None
    for title in section_titles:
        date = isDate(title)
    return date

class Context:
<<<<<<< HEAD
    def __init__(self, sub_line):#, isPl=False):
        #if isPl:
            #self.text = sub_line
        #else:
=======
    def __init__(self, sub_line):
>>>>>>> 8e25dd39d45b7ce7368cf03ad5e5959db5fdd5aa
        self.text = sub_line.text
        #[s.text if isinstance(s,Line) else s for s in line.sub_lines]
        self.text = cleanText(self.text, isQuote=False)
        if len(self.text) < 6 or any([char for char in self.text if char in forbidden_non_alphanumerics_for_context]):
            self.text = None 
        self.entities = sub_line.links
        self.external_links = sub_line.external_links


<<<<<<< HEAD
class untemplatedQuote:   
    def __init__(self, section_titles, line, id, n, lang, wikiquote_id):
=======


class untemplatedQuote:   
    def __init__(self, section_titles, line, id, n, lang):
>>>>>>> 8e25dd39d45b7ce7368cf03ad5e5959db5fdd5aa
        self.id = id+"_"+lang+"_"+str(n)
        self.section_titles = section_titles
        self.section_titles = [cleanText(title, isQuote=False) for title in self.section_titles]
        self.entities = line.links
        self.contexts = []
        self.page_language = lang
<<<<<<< HEAD
        self.wikiquote_id = wikiquote_id
        self.wikiquote_url = self.page_language+".wikiquote.org/wiki/"+ ("_").join(self.wikiquote_id.split(" "))
        if lang == "pl":
            for sub_line in line.sub_lines:
                if isinstance(sub_line,Line):
                    if "Opis" in sub_line.text:
                        self.direct_context = sub_line.text[6:] 
                        #self.contexts.append(Context(sub_line.text[6:], isPl=True))
                    if "Źródło" in sub_line.text:
                        self.source = sub_line.text[8:]
                        #self.contexts.append(Context(sub_line.text[8:], isPl=True ))
                    if "Zobacz też" in sub_line.text:
                        continue
        else:
            for sub_line in line.sub_lines:
                if isinstance(sub_line,Line):
                    self.contexts.append(Context(sub_line))
=======
        for sub_line in line.sub_lines:
            if isinstance(sub_line,Line):
                self.contexts.append(Context(sub_line))
>>>>>>> 8e25dd39d45b7ce7368cf03ad5e5959db5fdd5aa
        self.footnotes = [s.text if isinstance(s,Line) else s for s in line.footnotes]
        self.external_links = line.external_links
        self.segment_embeddings=[]
        self.embedding = None
        self.date = None
        #self.date=getDate(self.section_titles)
        self.original = None
        if lang == "de":
            self.quote = line.text.split('" -')[:-1]
            if isinstance(self.quote, list):
                self.quote = "".join(self.quote)
            self.direct_context = line.text.split('" -')[-1]
        else:
            self.quote = line.text
        #if the first subline is in a different language, consider it to be the original quote
        if line.bold == None:
            line.bold = []
        if line.italic == None:
            line.italic = []
        self.quote_segments = [line.text[segment[0]:segment[1]] for segment in line.bold] + [line.text[segment[0]:segment[1]] for segment in line.italic] 
        if self.quote:
            self.quote = cleanText(self.quote, isQuote=True)
            if self.quote:
                if len(self.quote) < 6 or any([char for char in self.quote if char in forbidden_non_alphanumerics_for_quotes]):
                     self.quote=None
        
        if self.quote:
            try:
                self.language=detect(self.quote)
            except langdetect.lang_detect_exception.LangDetectException:
                self.language = None
                pass
            self.okay = True
        else:
            self.language = None
            self.okay = False
        self.misattributed = False
        self.about = False

        if self.language:
            if isinstance(self.language,Line):
                self.language = self.language.text
        for title in self.section_titles:
            for x in about_list:
                if x.lower() in title.lower():
                    self.about = True
            if title.lower() in misattributed:
                self.misattributed = True
            if title.lower() in about_list:
                self.about = True

        #if self.quote_segments:
            #self.segment_embeddings = [model.encode(segment, device='cuda') for segment in self.quote_segments]
        #else:
            #self.embedding = model.encode(self.quote, device='cuda')
        #self.language = (translator.detect(self.quote).lang, translator.detect(self.quote).confidence)
        #translation = translator.translate(self.quote)
        #self.sentiment = sia.polarity_scores(translation.text)
<<<<<<< HEAD
        if isinstance(self.quote, str):
            if len(self.quote) > 5:
                self.sentiment = sentiment_task(self.quote[:514])
=======
>>>>>>> 8e25dd39d45b7ce7368cf03ad5e5959db5fdd5aa
        
    def __bool__(self):
        return self.okay and not self.about



class templatedQuote():
    def __init__(self, *args, **kwargs):
        self.direct_context = None
        self.quote_segments = None
<<<<<<< HEAD
        #self.wikiquote_source = 
        self.section_titles = args[3]
        self.wikiquote_id = args[4]
=======
        self.section_titles = args[3]
>>>>>>> 8e25dd39d45b7ce7368cf03ad5e5959db5fdd5aa
        self.section_titles = [cleanText(title, isQuote=False) for title in self.section_titles]
        self.sentiment = None
        self.date = None
        self.language = None
        self.page_language = args[2]
<<<<<<< HEAD
        self.wikiquote_url = self.page_language+".wikiquote.org/wiki/"+ ("_").join(self.wikiquote_id.split(" "))
=======
>>>>>>> 8e25dd39d45b7ce7368cf03ad5e5959db5fdd5aa
        self.id = args[0]+"_t_"+args[2]+"_"+str(args[1])
        for key in kwargs:
            if key.lower() in attrDict:
                setattr(self, attrDict[key.lower()], kwargs[key])
        try:
            self.quote = self.quote.text
            self.quote = cleanText(self.quote, isQuote=True)
            if self.quote:
                if len(self.text) < 6 or any([char for char in self.quote if char in forbidden_non_alphanumerics_for_quotes]):
<<<<<<< HEAD
                    self.quote = None
                    self.okay = False
            else:
                self.okay = False
=======
                     self.quote=None
>>>>>>> 8e25dd39d45b7ce7368cf03ad5e5959db5fdd5aa
            if not self.language:
                try:
                    self.language=detect(self.quote)
                except langdetect.lang_detect_exception.LangDetectException:
                    self.language = None
                    pass
            self.embedding = None #model.encode(self.quote, device='cuda')
            #if not self.date:
                #self.date=getDate(self.section_titles)
            #sia = SentimentIntensityAnalyzer()
            #self.language = (translator.detect(self.quote).lang, translator.detect(self.quote).confidence)
            #translation = translator.translate(self.quote)
            #self.sentiment = sia.polarity_scores(translation.text)
<<<<<<< HEAD
            if isinstance(self.quote, str):
                if len(self.quote) > 5:
                    self.sentiment = sentiment_task(self.quote[:514])
=======
>>>>>>> 8e25dd39d45b7ce7368cf03ad5e5959db5fdd5aa
            self.about = False
            self.misattributed = False

            if self.language:
                if isinstance(self.language,Line):
                    self.language = self.language.text
            for title in self.section_titles:
                for x in about_list:
                    if x.lower() in title.lower():
                        self.about = True
                if title.lower() in misattributed:
                    self.misattributed = True
                if title.lower() in about_list:
                    self.about = True

<<<<<<< HEAD
            #self.okay = True
=======
            self.okay = True
>>>>>>> 8e25dd39d45b7ce7368cf03ad5e5959db5fdd5aa
        except AttributeError:
            self.okay=False

    def __bool__(self):
        return self.okay and not self.about

            
            
            
            





"""
no template languages:
["eo","en","de","tr","no","hu","ta","he","pt","pl","cy","it","ar","bs","lt","ku","gl","te","hi","sa","sl","hr","sq","sk","ur","sr","eu","el","vi","uz","es","id","th","az","li",kn]
["ja","si"]> mostly no template
full template languages:
["fr","da","nl","be","is","ca","bg","da","ka"]
hybrid:
["uk","ru","sv","et"]
only context template languages:
["ko","fa","cs","fi", "hy"]
["zh"]> mostly no template for lines
?
'ml', 'gu', 'ro', 'sah', 'su', 'la'
????
["nn"] 

# nl, template : "vertaald citaat"
source = "bron"
cited = "aangehaald"
language = "taal"
remark = "opmerking"
quote = "tekst"
# fa
author = "نویسنده"
# si   
quote = "simple"
# ka Template : "Q"
quote = "ციტატა"
# fr, Template: "citation"
quote = "original"
translation = "citation"
context = "précisions"
language = "langue"
# fr, Template: "Réf"
date = "date"
release = "parution"
source = "source"
# da, Template: "citat"
quote = "1"
# ko, Template: "웹 인용"
posting_date = "작성일자"
title =  "제목"
publisher = "출판사"
url = "url"
# ko, Template: "뉴스 인용"
posting_date = "작성일자"
title =  "제목"
publisher = "출판사"
url = "url"
#cs, Template: "Citace monografie"
translators = "překladatelé"
title = "titul"
surname = "příjmení"
location = "místo"
isbn = "isbn"
publisher = "vydavatel"
name = "jméno"
year = "rok"
#cs, Template: "Citace elektronického periodika"
title = "titul"
surname = "příjmení"
access_date = "datum přístupu"
release_date = "datum vydání"
periodical = "periodikum"
name = "jméno"
url = "url"
#cs, Template: "Citace periodika"
issn = "issn"
periodical = "periodikum"
month = "měsíc"
page = "strany"
year = "rok"
#uk, Template: "Q"
quote = "Цитата"
author = "Автор"
comment = "Коментар"
#uk, Template: "q"
quote = "1"
#,Template: Q
quote = "1"
comment = "Комментарий"
original = "Original"
#sv, Template: citat
quote = "1"
quote = "2"
#be, Template : q
comment = "Каментар"
quote = "Цытата"
author = "Аўтар"
#be, Template: "крыніца" (source)
#fi, Template: "Verkkoviite"
author = "Tekijä"
referenced = "Viitattu"
address = "Osoite"
publication = "Julkaisu"
title = "Nimeke"
date = "Ajankohta"
#it, Template: "NDR" , Template: "Int"
context = "1" # on Line level
#is, Template: Tilvitnun Q30875
quote = "1"
explanation = "útskýring"
language = "language"
original = "frummál"
#ca, Template: "Cita"
quote = "cita"
original = "original"
date = "data"
location = "lloc"
language = "idioma"
notes = "notes"
#bg, Template: "Цитат"
quote = "1" #and other numbers of course
#et, Template: "halliga"
quote = "1"
#ja, Template: "lang"??
#hy, Template: "cite book"
editor = "editor"
year = "year"
publisher = "publisher"
page = "page"
title = "title"
ISBN = "ISBN"
#zh, Template: "cite web"
archive_date = "archive-date"
accessDate = "accessdate"
archive_url = "archive-url"
title = "title"
url = "url"
#zh, Template: "cite news"
archive_date = "archive-date"
accessDate = "access-date"
archive_url = "archive-url"
title = "title"
url = "url"
#zh: lines starting with  "原文:" (original)
#zh, Template:"lang" under a line
"""