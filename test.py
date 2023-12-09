# str = str.lower(input('Enter word: '))
#
# flag = 0
#
# for char in str:
#     if (str.count(char)>1):
#         flag = 1
#         break
# if flag == 0:
#     print(' It is an isogram')
#
# else:
#     print(' It\'s not an isogram')
#######################################
# text = str.lower(input('Enter word: '))
#
# if len(set(text)) != len(text):
#     print(' It\'s not an isogram')
#
# else:
#     print(' It is an isogram')


# def reversed2(variable):
#     res=[]
#     for i in range(len(variable)-1,-1,-1):
#         res.append(variable[i])
#     return res




# def reversed4(variable):
#     res=''.join(reversed(variable))
#     return res
#
# n = reversed4(input())
# print(n)


# n = input()[::-1]
# print(n)



# def reverse_words(sentence):
#     return ' '.join(word[::-1] for word in sentence.split())
#
# input_sentence = input()
# reversed_sentence = reverse_words(input_sentence)
# print(reversed_sentence)


reversed_sentence = ' '.join(word[::-1] for word in input().split())
