# -*- coding: utf-8 -*-
''' strings.py - Constant strings that need internationalization.
    This file should only be imported after gettext has been correctly initialized
    and installed in the global namespace. '''

from mcomix.constants import ZIP, RAR, TAR, GZIP, BZIP2, XZ, PDF, SEVENZIP, LHA, ZIP_EXTERNAL

ARCHIVE_DESCRIPTIONS = {
        ZIP: 'ZIP archive',
        RAR: 'RAR archive',
        TAR: 'Tar archive',
        GZIP: 'Gzip compressed tar archive',
        BZIP2: 'Bzip2 compressed tar archive',
        XZ: 'XZ compressed tar archive',
        PDF: 'PDF document',
        SEVENZIP: '7z archive',
        LHA: 'LHA archive',
        ZIP_EXTERNAL: 'ZIP archive',
}

AUTHORS = (
        ('Pontus Ekberg', 'Original vision/developer of Comix'),
        ('Louis Casillas', 'MComix developer'),
        ('Moritz Brunner', 'MComix developer'),
        ('Ark', 'MComix developer'),
        ('Benoit Pierre', 'MComix developer'),
)

TRANSLATORS = (
        ('Emfox Zhou', 'Simplified Chinese translation'),
        ('Xie Yanbo', 'Simplified Chinese translation'),
        ('Zach Cheung', 'Simplified Chinese translation'),
        ('Manuel Quiñones', 'Spanish translation'),
        ('Carlos Feliu', 'Spanish translation'),
        ('Marcelo Góes', 'Brazilian Portuguese translation'),
        ('Christoph Wolk', 'German translation and Nautilus thumbnailer'),
        ('Chris Leick', 'German translation'),
        ('Raimondo Giammanco', 'Italian translation'),
        ('Giovanni Scafora', 'Italian translation'),
        ('GhePeU', 'Italian translation'),
        ('Arthur Nieuwland', 'Dutch translation'),
        ('Achraf Cherti', 'French translation'),
        ('Benoît H.', 'French translation'),
        ('Joseph M. Sleiman', 'French translation'),
        ('Frédéric Chateaux', 'French translation'),
        ('Kamil Leduchowski', 'Polish translatin'),
        ('Darek Jakoniuk', 'Polish translation'),
        ('Paul Chatzidimitriou', 'Greek translation'),
        ('Carles Escrig Royo', 'Catalan translation'),
        ('Hsin-Lin Cheng', 'Traditional Chinese translation'),
        ('Wayne Su', 'Traditional Chinese translation'),
        ('Mamoru Tasaka', 'Japanese translation'),
        ('Keita Haga', 'Japanese translation'),
        ('Toshiharu Kudoh', 'Japanese translation'),
        ('Ernő Drabik', 'Hungarian translation'),
        ('Artyom Smirnov', 'Russian translation'),
        ('Евгений Лежнин', 'Russian translation'),
        ('Adrian C.', 'Croatian translation'),
        ('김민기', 'Korean translation'),
        ('Gyeongmin Bak', 'Korean translation'),
        ('Minho Jeung', 'Korean translation'),
        ('Maryam Sanaat', 'Persian translation'),
        ('Andhika Padmawan', 'Indonesian translation'),
        ('Jan Nekvasil', 'Czech translation'),
        ('Олександр Заяц', 'Ukrainian translation'),
        ('Roxerio Roxo Carrillo', 'Galician translation'),
        ('Martin Karlsson', 'Swedish translation'),
        ('Jonatan Nyberg', 'Swedish translation'),
        ('Isratine Citizen', 'Hebrew translation'),
        ('Zygi Mantus', 'Lithuanian translation'),
)

ARTISTS = (
        ('Victor Castillejo', 'Icon design'),
)
