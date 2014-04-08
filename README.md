SQLog
=========
Проект находится в разработке.

SQLog - это компилятор языка Datalog в SQL.

Ограничения
----
  - Пока запрос будет состоять из одного правила
  - Никакой рекурсии
  - Имена предикатов - это имена таблиц
  - Имена столбцов указываются в конфиге

Технологии
----
Предполагается, что Python и MySQL.

Язык Datalog
----
Правило

    A(x,y,z) <- M(x,y,z,_,_,_) AND y+1=2*z
    
В правой части подцели реляционные либо арифметические (сравнение арифметических выражений).

Подцели могут быть с NOT и разделяются AND (арифметические подцели не могут быть с NOT, т.к. вместо = можно написать != и т д)

_ - это анонимная переменная. Не может быть в левой части

Правило безопасности:

> Любая переменная из правила должна упоминаться в реляционной подцели без NOT. В частности, любая переменная из левой части.

Если несколько правил, то результат - объединение.

Оператор NOT реализуется в SQL через NOT EXISTS (AND NOT EXISTS...)

Выражения тупо оставляем, только заменяем переменные на имена столбцов

Грамматика
----

<Правило> :== <Атом> <- <Правая часть>
<Правая часть> :== <Aтом> | NOT <Атом> | <Aтом> AND <Правая часть> | NOT <Атом> AND <Правая часть>
<Атом> :== <Имя предиката> ( <Список переменных> ) | <Сравнение>

<Список переменных> :== <Имя переменной> | <Имя переменной> , <Список переменных>
<Сравнение> :== <Всякая фигня>
<Всякая фигня> :== <Фиговина> | <Фиговина> <Всякая фигня>
<Фиговина> :== <Цифра> |  <Имя переменной> | <Знак операции (может и сравнение)> | <Скобки>