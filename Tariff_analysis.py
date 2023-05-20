#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd


# ### Откройте файл с данными и изучите общую информацию

# **Задание 1.** Откройте файл `/datasets/calls.csv`, сохраните датафрейм в переменную `calls`.

# In[3]:


calls = pd.read_csv('/datasets/calls.csv')


# **Задание 2.** Выведите первые 5 строк датафрейма `calls`.

# In[4]:


print(calls.head(5))


# **Задание 3.** Выведите основную информацию для датафрейма `calls` с помощью метода `info()`.

# In[5]:


print(calls.info())


# **Задание 4.** С помощью метода `hist()` выведите гистограмму для столбца с продолжительностью звонков. Подумайте о том, как распределены данные.

# In[6]:


calls['duration'].hist(bins=50)


# **Задание 5.** Откройте файл `/datasets/internet.csv`, сохраните датафрейм в переменную `sessions`.

# In[7]:


sessions = pd.read_csv('/datasets/internet.csv')


# **Задание 6.** Выведите первые 5 строк датафрейма `sessions`.

# In[8]:


print(sessions.head(5))


# **Задание 7.** Выведите основную информацию для датафрейма `sessions` с помощью метода `info()`. 

# In[11]:


print(sessions.info())


# **Задание 8.** С помощью метода `hist()` выведите гистограмму для столбца с количеством потраченных мегабайт.

# In[12]:


sessions['mb_used'].hist(bins=50)


# **Задание 9.** Откройте файл `/datasets/messages.csv`, сохраните датафрейм в переменную `messages`.

# In[13]:


messages = pd.read_csv('/datasets/messages.csv')


# **Задание 10.** Выведите первые 5 строк датафрейма `messages`.

# In[14]:


print(messages.head(5))


# **Задание 11.** Выведите основную информацию для датафрейма `messages` с помощью метода `info()`. 

# In[15]:


print(messages.info())


# **Задание 12.** Откройте файл `/datasets/tariffs.csv`, сохраните датафрейм в переменную `tariffs`.

# In[16]:


tariffs = pd.read_csv('/datasets/tariffs.csv')


# **Задание 13.** Выведите весь датафрейм `tariffs`.

# In[17]:


print(tariffs)


# **Задание 14.** Выведите основную информацию для датафрейма `tariffs` с помощью метода `info()`.

# In[18]:


print(tariffs.info())


# **Задание 15.** Откройте файл `/datasets/users.csv`, сохраните датафрейм в переменную `users`.

# In[19]:


users = pd.read_csv('/datasets/users.csv')


# **Задание 16.** Выведите первые 5 строк датафрейма `users`.

# In[20]:


print(users.head(5))


# **Задание 17.** Выведите основную информацию для датафрейма `users` с помощью метода `info()`.

# In[21]:


print(users.info())


# ### Подготовьте данные

# **Задание 18.**  Приведите столбцы
# 
# - `reg_date` из таблицы `users`
# - `churn_date` из таблицы `users`
# - `call_date` из таблицы `calls`
# - `message_date` из таблицы `messages`
# - `session_date` из таблицы `sessions`
# 
# к новому типу с помощью метода `to_datetime()`.

# In[22]:


users['reg_date'] = pd.to_datetime(users['reg_date'])
users['churn_date'] = pd.to_datetime(users['churn_date'])
calls['call_date'] = pd.to_datetime(calls['call_date'])
messages['message_date'] = pd.to_datetime(messages['message_date'])
sessions['session_date'] = pd.to_datetime(sessions['session_date'])


# **Задание 19.** В данных вы найдёте звонки с нулевой продолжительностью. Это не ошибка: нулями обозначены пропущенные звонки, поэтому их не нужно удалять.
# 
# Однако в столбце `duration` датафрейма `calls` значения дробные. Округлите значения столбца `duration` вверх с помощью метода `numpy.ceil()` и приведите столбец `duration` к типу `int`.

# In[23]:


import numpy as np

calls['duration'] = np.ceil(calls['duration']).astype('int') # округление значений столбца duration с помощью np.ceil() и приведение типа к int


# **Задание 20.** Удалите столбец `Unnamed: 0` из датафрейма `sessions`. Столбец с таким названием возникает, когда данные сохраняют с указанием индекса (`df.to_csv(..., index=column)`). Он сейчас не понадобится.

# In[24]:


sessions = sessions.drop(columns=['Unnamed: 0'])


# **Задание 21.** Создайте столбец `month` в датафрейме `calls` с номером месяца из столбца `call_date`.

# In[25]:


calls['month'] = calls['call_date'].dt.month


# **Задание 22.** Создайте столбец `month` в датафрейме `messages` с номером месяца из столбца `message_date`.

# In[26]:


messages['month'] = messages['message_date'].dt.month


# **Задание 23.** Создайте столбец `month` в датафрейме `sessions` с номером месяца из столбца `session_date`.

# In[27]:


sessions['month'] = sessions['session_date'].dt.month


# **Задание 24.** Посчитайте количество сделанных звонков разговора для каждого пользователя по месяцам.

# In[2]:


calls_per_month = calls.groupby(['user_id','month']).agg(calls=('duration', 'count'))


# In[ ]:


calls_per_month.head(30)# вывод 30 первых строк на экран


# **Задание 25.** Посчитайте количество израсходованных минут разговора для каждого пользователя по месяцам и сохраните в переменную `minutes_per_month`. Вам понадобится
# 
# - сгруппировать датафрейм с информацией о звонках по двум столбцам — с идентификаторами пользователей и номерами месяцев;
# - после группировки выбрать столбец `duration`
# - затем применить метод для подсчёта суммы.
# 
# Выведите первые 30 строчек `minutes_per_month`.

# In[ ]:



minutes_per_month = calls.groupby(['user_id','month']).agg(minutes=('duration', 'sum'))


# In[ ]:


print(minutes_per_month.head(30))


# **Задание 26.** Посчитайте количество отправленных сообщений по месяцам для каждого пользователя и сохраните в переменную `messages_per_month`. Вам понадобится
# 
# - сгруппировать датафрейм с информацией о сообщениях по двум столбцам — с идентификаторами пользователей и номерами месяцев;
# - после группировки выбрать столбец `message_date`;
# - затем применить метод для подсчёта количества.
# 
# Выведите первые 30 строчек `messages_per_month`.

# In[ ]:


messages_per_month = messages.groupby(['user_id', 'month']).agg(messages=('message_date', 'count')) # подсчёт количества отправленных сообщений для каждого пользователя по месяцам


# In[ ]:


print(messages_per_month.head(30)) # вывод первых 30 строк на экран


# **Задание 27.** Посчитайте количество потраченных мегабайт по месяцам для каждого пользователя и сохраните в переменную `sessions_per_month`. Вам понадобится
# 
# - сгруппировать датафрейм с информацией о сообщениях по двум столбцам — с идентификаторами пользователей и номерами месяцев;
# - затем применить метод для подсчёта суммы: `.agg({'mb_used': 'sum'})`

# In[ ]:


sessions_per_month = sessions.groupby(['user_id', 'month']).agg({'mb_used': 'sum'}) # подсчёт потраченных мегабайт для каждого пользователя по месяцам


# In[ ]:


print(sessions_per_month.head(30)) # вывод первых 30 строк на экран


# ### Анализ данных и подсчёт выручки

# Объединяем все посчитанные выше значения в один датафрейм `user_behavior`.
# Для каждой пары «пользователь — месяц» будут доступны информация о тарифе, количестве звонков, сообщений и потраченных мегабайтах.

# In[ ]:


users['churn_date'].count() / users['churn_date'].shape[0] * 100


# Расторгли договор 7.6% клиентов из датасета

# In[ ]:


user_behavior = calls_per_month    .merge(messages_per_month, left_index=True, right_index=True, how='outer')    .merge(sessions_per_month, left_index=True, right_index=True, how='outer')    .merge(minutes_per_month, left_index=True, right_index=True, how='outer')    .reset_index()    .merge(users, how='left', left_on='user_id', right_on='user_id')
user_behavior.head()


# Проверим пропуски в таблице `user_behavior` после объединения:

# In[ ]:


user_behavior.isna().sum()


# Заполним образовавшиеся пропуски в данных:

# In[ ]:


user_behavior['calls'] = user_behavior['calls'].fillna(0)
user_behavior['minutes'] = user_behavior['minutes'].fillna(0)
user_behavior['messages'] = user_behavior['messages'].fillna(0)
user_behavior['mb_used'] = user_behavior['mb_used'].fillna(0)


# Присоединяем информацию о тарифах

# In[ ]:


# переименование столбца tariff_name на более простое tariff

tariffs = tariffs.rename(
    columns={
        'tariff_name': 'tariff'
    }
)


# In[ ]:


user_behavior = user_behavior.merge(tariffs, on='tariff')


# Считаем количество минут разговора, сообщений и мегабайт, превышающих включённые в тариф
# 

# In[ ]:


user_behavior['paid_minutes'] = user_behavior['minutes'] - user_behavior['minutes_included']
user_behavior['paid_messages'] = user_behavior['messages'] - user_behavior['messages_included']
user_behavior['paid_mb'] = user_behavior['mb_used'] - user_behavior['mb_per_month_included']

for col in ['paid_messages', 'paid_minutes', 'paid_mb']:
    user_behavior.loc[user_behavior[col] < 0, col] = 0


# Переводим превышающие тариф мегабайты в гигабайты и сохраняем в столбец `paid_gb`

# In[ ]:


user_behavior['paid_gb'] = np.ceil(user_behavior['paid_mb'] / 1024).astype(int)


# Считаем выручку за минуты разговора, сообщения и интернет

# In[ ]:


user_behavior['cost_minutes'] = user_behavior['paid_minutes'] * user_behavior['rub_per_minute']
user_behavior['cost_messages'] = user_behavior['paid_messages'] * user_behavior['rub_per_message']
user_behavior['cost_gb'] = user_behavior['paid_gb'] * user_behavior['rub_per_gb']


# Считаем помесячную выручку с каждого пользователя, она будет храниться в столбце `total_cost`

# In[ ]:


user_behavior['total_cost'] =       user_behavior['rub_monthly_fee']    + user_behavior['cost_minutes']    + user_behavior['cost_messages']    + user_behavior['cost_gb']


# Датафрейм `stats_df` для каждой пары «месяц — тариф» будет хранить основные характеристики

# In[ ]:


# сохранение статистических метрик для каждой пары месяц-тариф
# в одной таблице stats_df (среднее значение, стандартное отклонение, медиана)

stats_df = user_behavior.pivot_table(
            index=['month', 'tariff'],\
            values=['calls', 'minutes', 'messages', 'mb_used'],\
            aggfunc=['mean', 'std', 'median']\
).round(2).reset_index()

stats_df.columns=['month', 'tariff', 'calls_mean', 'sessions_mean', 'messages_mean', 'minutes_mean',
                                     'calls_std',  'sessions_std', 'messages_std', 'minutes_std', 
                                     'calls_median', 'sessions_median', 'messages_median',  'minutes_median']

stats_df.head(10)


# Распределение среднего количества звонков по видам тарифов и месяцам

# In[ ]:


import seaborn as sns

ax = sns.barplot(x='month',
            y='calls_mean',
            hue="tariff",
            data=stats_df,
            palette=['lightblue', 'blue'])

ax.set_title('Распределение количества звонков по видам тарифов и месяцам')
ax.set(xlabel='Номер месяца', ylabel='Среднее количество звонков');


# In[ ]:


import matplotlib.pyplot as plt

user_behavior.groupby('tariff')['calls'].plot(kind='hist', bins=35, alpha=0.5)
plt.legend(['Smart', 'Ultra'])
plt.xlabel('Количество звонков')
plt.ylabel('Количество клиентов')
plt.show()


# Распределение средней продолжительности звонков по видам тарифов и месяцам

# In[ ]:


ax = sns.barplot(x='month',
            y='minutes_mean',
            hue="tariff",
            data=stats_df,
            palette=['lightblue', 'blue'])

ax.set_title('Распределение продолжительности звонков по видам тарифов и месяцам')
ax.set(xlabel='Номер месяца', ylabel='Средняя продолжительность звонков');


# In[ ]:


user_behavior[user_behavior['tariff'] =='smart']['minutes'].hist(bins=35, alpha=0.5, color='green')
user_behavior[user_behavior['tariff'] =='ultra']['minutes'].hist(bins=35, alpha=0.5, color='blue');


# Средняя длительность разговоров у абонентов тарифа Ultra больше, чем у абонентов тарифа Smart. В течение года пользователи обоих тарифов увеличивают среднюю продолжительность своих разговоров. Рост средней длительности разговоров у абонентов тарифа Smart равномерный в течение года. Пользователи тарифа Ultra не проявляют подобной линейной стабильности. Стоит отметить, что феврале у абонентов обоих тарифных планов наблюдались самые низкие показатели.

# Распределение среднего количества сообщений по видам тарифов и месяцам

# In[ ]:


ax = sns.barplot(x='month',
            y='messages_mean',
            hue="tariff",
            data=stats_df,
            palette=['lightblue', 'blue']
)

ax.set_title('Распределение количества сообщений по видам тарифов и месяцам')
ax.set(xlabel='Номер месяца', ylabel='Среднее количество сообщений');


# In[ ]:


user_behavior[user_behavior['tariff'] =='smart']['messages'].hist(bins=35, alpha=0.5, color='green')
user_behavior[user_behavior['tariff'] =='ultra']['messages'].hist(bins=35, alpha=0.5, color='blue');


# В среднем пользователи тарифа Ultra отправляют больше сообщений — почти на 20 сообщений больше, чем пользователи тарифа Smart. Количество сообщений в течение года на обоих тарифах растёт. Динамика по отправке сообщений схожа с тенденциями по длительности разговоров: в феврале отмечено наименьшее количество сообщений за год и пользователи тарифа Ultra также проявляют нелинейную положительную динамику.

# In[ ]:


ax = sns.barplot(x='month',
            y='sessions_mean',
            hue='tariff',
            data=stats_df,
            palette=['lightblue', 'blue']
)

ax.set_title('Распределение количества потраченного трафика (Мб) по видам тарифов и месяцам')
ax.set(xlabel='Номер месяца', ylabel='Среднее количество мегабайт');


# Сравнение потраченных мегабайт среди пользователей тарифов Smart и Ultra

# In[ ]:


user_behavior[user_behavior['tariff'] =='smart']['mb_used'].hist(bins=35, alpha=0.5, color='green')
user_behavior[user_behavior['tariff'] =='ultra']['mb_used'].hist(bins=35, alpha=0.5, color='blue');


# Меньше всего пользователи использовали интернет в январе, феврале и апреле. Чаще всего абоненты тарифа Smart тратят 15–17 Гб, а абоненты тарифного плана Ultra — 19–21 ГБ.

# ### Проверка гипотез

# **Задание 28.** Проверка гипотезы: средняя выручка пользователей тарифов «Ультра» и «Смарт» различается;
# 
# ```
# H_0: Выручка (total_cost) пользователей "Ультра" = выручка (total_cost) пользователей "Смарт"`
# H_a: Выручка (total_cost) пользователей "Ультра" ≠ выручка (total_cost) пользователей "Смарт"`
# alpha = 0.05
# ```

# In[ ]:


from scipy import stats as st


# In[ ]:


results = st.ttest_ind(
    user_behavior.loc[user_behavior.tariff == 'ultra', 'total_cost'],
    user_behavior.loc[user_behavior.tariff == 'smart', 'total_cost'], 
    equal_var=False)
 
alpha = 0.05
 
print(results.pvalue)
 
if results.pvalue < alpha:
    print("Отвергаем нулевую гипотезу")
else:
    print("Не получилось отвергнуть нулевую гипотезу")


# **Задание 29.** Проверка гипотезы: средняя выручка с пользователей из Москвы отличается от выручки c пользователей других регионов; 
# 
# ```
# H_0: Выручка (total_cost) пользователей из Москвы = выручка (total_cost) пользователей не из Москвы`
# H_1: Выручка (total_cost) пользователей из Москвы ≠ выручка (total_cost) пользователей не из Москвы`
# alpha = 0.05
# ```

# In[ ]:


msk = user_behavior[user_behavior['city'] == 'Москва']['total_cost']
other_city = user_behavior[user_behavior['city'] != 'Москва']['total_cost']
# вызов метода для проверки гипотезы
results = st.ttest_ind(msk, other_city)

# задайте значение уровня значимости
alpha = .05
# вывод значения p-value на экран
print(results.pvalue)
# условный оператор с выводом строки с ответом
if results.pvalue < alpha:
    print('Отвергаем нулевую гипотезу')
else:
    print('Не получилось отвергнуть нулевую гипотезу')

