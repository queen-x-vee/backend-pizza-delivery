from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from models import Order,   User
from schemas import OrderModel, OrderStatusModel
from fastapi.exceptions import HTTPException
from database import engine, Session
from fastapi.encoders import jsonable_encoder

order_router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

session = Session(bind = engine)

@order_router.get("/")
async def hello(Authorize:AuthJWT = Depends()):
    #to protect this route, write the following code

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    return {"message": "Hello World"}


@order_router.post("/order", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderModel, Authorize:AuthJWT = Depends()):
    """
        ## Create a new order
        This endpoint is used to create a new order.
        It requires the user to be logged in.
        It requires the following
        - quantity: integer
        - pizza_size: string
        

    """

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    #current_user = session.query(User).filter(User.username == order.username).first()

    current_user=Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    new_order = Order(
        pizza_size=order.pizza_size,
        quantity = order.quantity
    )

    #now attach the order to the user

    new_order.user = user

    #save this with session

    session.add(new_order)

    session.commit()

    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "order_status": new_order.order_status
    }

    return jsonable_encoder(response)


   

@order_router.get("/orders")
async def get_all_orders(Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    current_user=Authorize.get_jwt_subject()

    user= session.query(User).filter(User.username==current_user).first()

    if user.is_staff:
        orders= session.query(Order).all()

        return jsonable_encoder(orders)
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to view this")


@order_router.get("/orders/{id}")
async def get_order(id: int, Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    current_user=Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        order = session.query(Order).filter(Order.id == id).first()

        return jsonable_encoder(order)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to view this order")


#get a specific user orders

@order_router.get("/user/orders")
async def get_user_orders(Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    current_user=Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    return jsonable_encoder(user.orders)



    
#get a current user's specific order

@order_router.get("/user/order/{id}" )
async def get_specific_order(id: int, Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    current_user=Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    orders = user.orders

    for order in orders:
        if order.id == id:
            return jsonable_encoder(order)
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")


@order_router.put("/order/update/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_order(id: int, order:OrderModel, Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    order_to_update = session.query(Order).filter(Order.id == id).first()

    order_to_update.quantity=order.quantity
    order_to_update.pizza_size=order.pizza_size

    session.commit()

    response = {
        "id": order_to_update.id,
        "quantity": order_to_update.quantity,
        "pizza_size": order_to_update.pizza_size,
        "order_status": order_to_update.order_status
    }

    return jsonable_encoder(response)





@order_router.patch("/order/update/{id}", status_code=status.HTTP_202_ACCEPTED)

async def update_order_status(id: int, order_status:OrderStatusModel, Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    current_user=Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        order_to_update = session.query(Order).filter(Order.id == id).first()

        order_to_update.order_status=order_status.order_status

        session.commit()

        response = {
            "id": order_to_update.id,
            "quantity": order_to_update.quantity,
            "pizza_size": order_to_update.pizza_size,
            "order_status": order_to_update.order_status


        }

        return jsonable_encoder(response)
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to update this order")
    


#delete an order

@order_router.delete("/order/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(id: int, Authorize:AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    order_to_delete = session.query(Order).filter(Order.id == id).first()

    session.delete(order_to_delete)

    session.commit()

    return order_to_delete







